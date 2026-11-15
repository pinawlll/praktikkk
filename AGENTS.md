# Aturan Alur Kerja Git

## Remote
- `origin` = https://github.com/pinawlll/praktikkk.git

## Aturan wajib: review & konfirmasi sebelum push
Setiap perubahan pada repo ini **wajib** melalui alur berikut:

1. Buat perubahan (edit/tambah/hapus file) → `git status` dan `git diff` ditampilkan.
2. Tunjukkan ringkasan perubahan: daftar file, statistik diff (`git diff --stat` / `git diff --cached --stat`), dan poin penting perubahannya.
3. **Berhenti dan minta konfirmasi eksplisit dari pemilik repo.**
4. Hanya setelah konfirmasi diberikan: `git push origin <branch>`.
5. Jika tidak ada konfirmasi, jangan push. Jangan pernah `push --force` atau push ke branch lain tanpa izin.

Commit lokal boleh dibuat, tetapi push ke GitHub selalu menunggu persetujuan.
