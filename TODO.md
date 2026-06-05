# TODO - Harga Barang & Foto

## Step 1
- [x] Analisis struktur app.py, database/init_db.py, templates/admin.html, templates/user.html

## Step 2
- [x] Update model `InventoryItem` untuk menambah `harga` dan `foto`


## Step 3
- [ ] Update model `Rental` agar menyimpan snapshot `harga` dan `foto` saat rental dibuat


## Step 4
- [ ] Update routing/logic di `app.py`:
  - [ ] Tambah konfigurasi upload
  - [ ] Proses input harga & upload foto di `/admin/items/add`
  - [ ] Proses simpan `harga` & `foto` snapshot ke `Rental` pada `/user/rentals/add`

## Step 5
- [ ] Update templates:
  - [ ] `templates/admin.html` (form + tabel barang: harga & preview foto)
  - [ ] `templates/user.html` (tabel rental: harga & foto)

## Step 6
- [ ] Jalankan app & verifikasi end-to-end:
  - [ ] Admin tambah barang dengan harga & foto
  - [ ] User sewa dan lihat harga & foto di daftar rental

