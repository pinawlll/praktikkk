# Lab Equipment Loan System

Backend REST API untuk mengelola master alat laboratorium, transaksi peminjaman, pengembalian alat, dan riwayat peminjaman mahasiswa.

## Teknologi

- Python 3.x
- Flask
- SQLite
- JSON (request dan response)

## Struktur Proyek

```
app/
├── __init__.py          # application factory, registrasi route & error handler
├── database.py          # koneksi SQLite, skema, perintah flask init-db
├── errors.py            # error yang dipetakan ke status HTTP
├── validators.py        # validasi payload request
├── repositories/        # query database (Item dan Loan)
├── services/            # aturan bisnis
└── routes/              # endpoint HTTP
instance/                # lokasi database SQLite (tidak masuk version control)
markdown/                # dokumen proyek
postman/                 # koleksi Postman
tests/                   # pengujian pytest
run.py                   # entry point
```

## Instalasi

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Inisialisasi Database

```bash
flask --app run.py init-db
```

Perintah ini membuat `instance/lab_equipment.db` beserta tabel `item` dan `loan`. Perintah aman dijalankan berulang.

Untuk mengulang dari database kosong, hapus file `instance/lab_equipment.db` lalu jalankan `init-db` kembali.

## Menjalankan Aplikasi

```bash
python run.py
```

Aplikasi berjalan di `http://127.0.0.1:5000`.

## Endpoint

| Method | Endpoint | Body | Sukses |
|---|---|---|---|
| GET | `/items` | - | `200 OK` |
| POST | `/items` | `{"name": "Multimeter", "total_stock": 10}` | `201 Created` |
| POST | `/loans` | `{"student_id": "20240001", "item_id": 1, "quantity": 2}` | `201 Created` |
| PUT | `/loans/{id}/return` | - | `200 OK` |
| GET | `/loans/student/{student_id}` | - | `200 OK` |

Format respons error: `{"error": "pesan"}` dengan status `400` atau `404` sesuai kondisi.

Contoh:

```bash
curl -X POST http://127.0.0.1:5000/items \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Multimeter\", \"total_stock\": 10}"

curl -X POST http://127.0.0.1:5000/loans \
  -H "Content-Type: application/json" \
  -d "{\"student_id\": \"20240001\", \"item_id\": 1, \"quantity\": 2}"

curl -X PUT http://127.0.0.1:5000/loans/1/return

curl http://127.0.0.1:5000/loans/student/20240001
```

## Pengujian

```bash
python -m pytest -q
```

## Postman

Impor `postman/collections/lab-equipment-loan.postman_collection.json`, atau jalankan melalui Postman CLI:

```bash
postman collection run postman/collections/lab-equipment-loan.postman_collection.json
```

Koleksi ini mengasumsikan database baru diinisialisasi (kosong) dan server berjalan di `http://127.0.0.1:5000`.
