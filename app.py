from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from database.init_db import init_db, register_models



app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"










@login_manager.user_loader
def load_user(user_id):
    # `User` class is defined dynamically by database.init_db.register_models(db)
    return User.query.get(int(user_id))



def ensure_default_admin():
    global User, InventoryItem, Rental

    # Default admin: admin / admin123 (change in production)
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()


@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("admin"))
        return redirect(url_for("user"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Username dan password wajib.", "error")
            return render_template("register.html")

        if User.query.filter_by(username=username).first():
            flash("Username sudah terdaftar.", "error")
            return render_template("register.html")

        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role="user",
        )
        db.session.add(user)
        db.session.commit()

        flash("Registrasi berhasil. Silakan login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Login gagal. Cek username/password.", "error")
            return render_template("login.html")

        login_user(user)
        return redirect(url_for("admin" if user.role == "admin" else "user"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Anda telah logout.", "success")
    return redirect(url_for("login"))


@app.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        flash("Akses ditolak.", "error")
        return redirect(url_for("user"))
    return render_template("admin.html", admin_section="items")



@app.route("/admin/users")
@login_required
def admin_users():
    if current_user.role != "admin":
        flash("Akses ditolak.", "error")
        return redirect(url_for("user"))
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin.html", admin_section="users", users=users)


@app.route("/admin/users/<int:user_id>/role", methods=["POST"])
@login_required
def admin_user_set_role(user_id):
    if current_user.role != "admin":
        flash("Akses ditolak.", "error")
        return redirect(url_for("user"))

    target = User.query.get_or_404(user_id)
    new_role = (request.form.get("role") or "").strip()
    if new_role not in ["admin", "user"]:
        flash("Role tidak valid.", "error")
        return redirect(url_for("admin_users"))

    # Hindari admin menghapus role dirinya menjadi kosong (masih tetap boleh set ke user).
    target.role = new_role
    db.session.commit()
    flash(f"Role user '{target.username}' diubah menjadi {new_role}.", "success")
    return redirect(url_for("admin_users"))


@app.route("/admin/rentals")
@login_required
def admin_rentals():
    if current_user.role != "admin":
        flash("Akses ditolak.", "error")
        return redirect(url_for("user"))

    rentals = Rental.query.order_by(Rental.created_at.desc()).all()
    return render_template(
        "admin.html",
        admin_section="rentals",
        rentals=rentals,
    )


@app.route("/admin/items")
@login_required
def admin_items():
    if current_user.role != "admin":
        flash("Akses ditolak.", "error")
        return redirect(url_for("user"))

    items = InventoryItem.query.order_by(InventoryItem.created_at.desc()).all()
    return render_template(
        "admin.html",
        admin_section="items",
        items=items,
    )


@app.route("/admin/items/add", methods=["POST"])
@login_required
def admin_items_add():
    if current_user.role != "admin":
        flash("Akses ditolak.", "error")
        return redirect(url_for("user"))

    nama_aset = (request.form.get("nama_aset") or "").strip()
    is_active_str = (request.form.get("is_active") or "true").strip().lower()

    if not nama_aset:
        flash("Nama aset wajib diisi.", "error")
        return redirect(url_for("admin_items"))

    is_active = is_active_str in ["1", "true", "yes", "y"]

    existing = InventoryItem.query.filter_by(nama_aset=nama_aset).first()
    if existing:
        existing.is_active = is_active
        db.session.commit()
        flash("Item sudah ada. Status diupdate.", "success")
        return redirect(url_for("admin_items"))

    item = InventoryItem(nama_aset=nama_aset, is_active=is_active)
    db.session.add(item)
    db.session.commit()
    flash("Item berhasil ditambahkan.", "success")
    return redirect(url_for("admin_items"))



@app.route("/admin/rentals/<int:rental_id>/delete", methods=["POST"])
@login_required
def admin_rentals_delete(rental_id):
    if current_user.role != "admin":
        flash("Akses ditolak.", "error")
        return redirect(url_for("user"))

    rental = Rental.query.get_or_404(rental_id)
    db.session.delete(rental)
    db.session.commit()
    flash("Rental berhasil dihapus.", "success")
    return redirect(url_for("admin_rentals"))


@app.route("/admin/rentals/<int:rental_id>/status", methods=["POST"])
@login_required
def admin_rentals_set_status(rental_id):
    if current_user.role != "admin":
        flash("Akses ditolak.", "error")
        return redirect(url_for("user"))

    rental = Rental.query.get_or_404(rental_id)

    new_status = (request.form.get("status") or "").strip()
    if new_status not in ["aktif", "selesai"]:
        flash("Status tidak valid.", "error")
        return redirect(url_for("admin_rentals"))

    rental.status = new_status
    db.session.commit()
    flash("Status rental berhasil diupdate.", "success")
    return redirect(url_for("admin_rentals"))



@app.route("/user")
@login_required
def user():
    rentals = (
        Rental.query.filter_by(user_id=current_user.id)
        .order_by(Rental.created_at.desc())
        .all()
    )
    items = InventoryItem.query.filter_by(is_active=True).order_by(InventoryItem.created_at.desc()).all()
    return render_template("user.html", rentals=rentals, items=items)




@app.route("/user/rentals/add", methods=["POST"])
@login_required
def user_rentals_add():
    item_id = request.form.get("item_id")
    tanggal_mulai_str = (request.form.get("tanggal_mulai") or "").strip()
    tanggal_selesai_str = (request.form.get("tanggal_selesai") or "").strip()
    status = (request.form.get("status") or "aktif").strip()

    if not item_id or not tanggal_mulai_str or not tanggal_selesai_str:
        flash("Semua field wajib diisi.", "error")
        return redirect(url_for("user"))

    if status not in ["aktif", "selesai"]:
        flash("Status tidak valid.", "error")
        return redirect(url_for("user"))

    try:
        item_id_int = int(item_id)
    except ValueError:
        flash("Item tidak valid.", "error")
        return redirect(url_for("user"))

    item = InventoryItem.query.get(item_id_int)
    if not item or not item.is_active:
        flash("Item tidak tersedia.", "error")
        return redirect(url_for("user"))

    try:
        tanggal_mulai = datetime.strptime(tanggal_mulai_str, "%Y-%m-%d")
        tanggal_selesai = datetime.strptime(tanggal_selesai_str, "%Y-%m-%d")
    except ValueError:
        flash("Format tanggal harus YYYY-MM-DD.", "error")
        return redirect(url_for("user"))

    rental = Rental(
        item_id=item.id,
        aset=item.nama_aset,
        tanggal_mulai=tanggal_mulai,
        tanggal_selesai=tanggal_selesai,
        status=status,
        user_id=current_user.id,
    )
    db.session.add(rental)
    db.session.commit()

    flash("Rental berhasil ditambahkan.", "success")
    return redirect(url_for("user"))




@app.route("/riwayat")
@login_required
def riwayat():
    rentals = Rental.query.filter_by(user_id=current_user.id).order_by(Rental.created_at.desc()).all()
    return render_template("riwayat.html", rentals=rentals)



def create_app():
    # Register models and bind them to app.py globals.
    global User, InventoryItem, Rental
    User, InventoryItem, Rental = register_models(db)

    with app.app_context():
        # If you change models, existing SQLite schema might be out-of-date.
        # For development, we drop and recreate tables to prevent runtime errors like
        # "no such column: rentals.harga".
        # WARNING: This deletes existing data in app.db.
        db.drop_all()
        init_db(db)
        ensure_default_admin()
    return app






if __name__ == "__main__":
    create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)


