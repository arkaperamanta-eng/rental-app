# Rental App (Flask)

Project structure sesuai permintaan:

```
rental_app/
│
├── app.py
├── config.py
├── requirements.txt
│
├── database/
│   └── init_db.py
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── admin.html
│   ├── user.html
│   └── riwayat.html
│
└── static/
    └── images/
```

## Run
1. `cd rental_app`
2. buat venv (opsional): `python -m venv venv`
3. install: `pip install -r requirements.txt`
4. `python app.py`

Catatan: Implementasi UI & routing utama dibuat sederhana (login/register/admin/user/riwayat) dan disiapkan untuk integrasi database.

