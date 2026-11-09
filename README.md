# Tugas Individu 5 – Flask: Cek Username (Routing + Template)

Studi kasus: **ZakClouth** (toko pakaian) – M Zaky Sai.
Username contoh yang sudah terdaftar: `zakysai`, `andi`, `citra`.

## Menjalankan
```bash
python -m venv venv
venv\Scripts\activate        # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
flask --app app run --debug
```
Buka http://127.0.0.1:5000

## Daftar Route
| URL | Fungsi | Keterangan |
|---|---|---|
| `/`, `/beranda` | index | halaman statis |
| `/tentang`, `/kontak` | tentang, kontak | halaman statis |
| `/produk` | produk | list produk (`{% for %}`) + pencarian `?q=` |
| `/produk/<int:id>` | detail_produk | converter `int` + `abort(404)` |
| `/cek/<username>` | cek_username | validasi min. 4 karakter (400 jika tidak valid) |
| `/cek?u=...` | cek_username | versi query string |
| `/user/<username>` | profil_user | profil; username pendek di-`redirect` ke `/cek/...`, tidak ada → 404 |
| `/daftar-user` | daftar_user | list member |
| `/home` | home_lama | `redirect` ke beranda |
| (404) | tidak_ditemukan | halaman error 404 kustom |

## Checklist Tugas
- [x] 4 route statis (beranda, tentang, produk, kontak)
- [x] `/cek/<username>` dan `/user/<username>` dengan validasi
- [x] `/produk/<int:id>` + `abort(404)`
- [x] `url_for` dan `redirect`
- [x] Custom 404
- [x] `base.html` (navbar + footer), semua halaman `{% extends %}`
- [x] Hasil cek memakai `{% if %}` 3 kondisi (tidak valid / tersedia / sudah dipakai)
- [x] `{% for %}` + filter Jinja2 (`title`, `upper`, `length`, `join`, `truncate`, `default`, filter kustom `rupiah`)
- [x] Semua link memakai `url_for`
