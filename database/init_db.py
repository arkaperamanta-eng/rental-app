from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash



def init_db(db):
    """Create tables for the app.

    db: instance of SQLAlchemy from Flask-SQLAlchemy.

    Important: models are defined in this module (single source of truth),
    so tables are created here as well.
    """
    # Ensure model metadata is registered before creating tables.
    db.create_all()


# --- Models (single source of truth) ---
# NOTE: These classes are bound to the `db` instance created in app.py.
# app.py must call `register_models(db)` once before calling `init_db(db)`.


def register_models(db):
    """Register ORM models on the provided SQLAlchemy instance.

    This must be called once after `db = SQLAlchemy(app)` is created.

    Returns: (User, InventoryItem, Rental)
    """
    global User, InventoryItem, Rental

    # expose to module globals so app.py can reference User/InventoryItem/Rental
    User, InventoryItem, Rental = None, None, None


    class User(db.Model, UserMixin):

        __tablename__ = "users"

        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)
        role = db.Column(db.String(20), nullable=False, default="user")  # 'admin' or 'user'
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        rentals = db.relationship(
            "Rental", back_populates="user", cascade="all, delete-orphan"
        )

    class InventoryItem(db.Model):
        __tablename__ = "inventory_items"

        id = db.Column(db.Integer, primary_key=True)
        nama_aset = db.Column(db.String(120), nullable=False, unique=True)

        # harga barang (untuk ditampilkan & disimpan snapshot saat rental dibuat)
        harga = db.Column(db.Numeric(10, 2), nullable=False, default=0)

        # nama file foto (mis: uuid.jpg) disimpan di static/images/
        foto = db.Column(db.String(255), nullable=True)

        is_active = db.Column(db.Boolean, nullable=False, default=True)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    class Rental(db.Model):
        __tablename__ = "rentals"

        id = db.Column(db.Integer, primary_key=True)

        item_id = db.Column(
            db.Integer, db.ForeignKey("inventory_items.id"), nullable=False
        )
        # snapshot nama aset saat rental dibuat (supaya historinya tetap jelas meski nama/item dinonaktifkan)
        aset = db.Column(db.String(120), nullable=False)

        # snapshot harga dan foto saat rental dibuat
        harga = db.Column(db.Numeric(10, 2), nullable=False, default=0)
        foto = db.Column(db.String(255), nullable=True)

        tanggal_mulai = db.Column(db.DateTime, nullable=False)
        tanggal_selesai = db.Column(db.DateTime, nullable=False)
        status = db.Column(db.String(20), nullable=False, default="aktif")  # 'aktif' / 'selesai'

        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
        created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        user = db.relationship("User", back_populates="rentals")
        item = db.relationship("InventoryItem")


    return User, InventoryItem, Rental


def ensure_default_admin(db, User):
    """Create default admin account if it doesn't exist."""
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

