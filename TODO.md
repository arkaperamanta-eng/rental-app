# TODO

## Perbaikan: Halaman Kelola Rental error
- [x] Identifikasi error: `sqlite3.OperationalError: no such column rentals.item_id` saat akses `/admin/rentals`.
- [x] Perbarui skema database agar tabel `rentals` punya kolom `item_id`.

- [ ] Pastikan perintah migrasi/refresh dijalankan tanpa merusak model.
- [x] Tes halaman `/admin/rentals` dan `/admin/items`.
- [ ] Tes penambahan rental dari halaman user (`/user`).


