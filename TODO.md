# TODO - Fitur tambah foto dan harga

## Langkah-langkah
- [x] Update `app.py`: route `/admin/items/add` terima `harga` dan upload `foto`, simpan ke `static/images/`, isi `InventoryItem.foto` dan `InventoryItem.harga`.
- [x] Update `templates/admin.html`: form Kelola Barang tambah field `harga` (wajib angka) dan input upload `foto`, set `enctype="multipart/form-data"`.
- [x] Update `app.py` pada `user_rentals_add`: pastikan snapshot rental mengisi `Rental.harga` dan `Rental.foto` dari `InventoryItem`.
- [x] Update `templates/user.html`: tampilkan harga pada daftar barang (foto belum ditampilkan di halaman user).
- [x] Validasi & error handling: pastikan jika foto tidak valid/ekstensi salah ditolak dengan flash message.
- [ ] Jalankan server dan test end-to-end.

