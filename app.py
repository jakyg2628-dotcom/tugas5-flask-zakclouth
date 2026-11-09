"""
Tugas Individu 5 - Routing & Template di Flask
Studi kasus: ZakClouth (pengecekan username member/pelanggan)
Disusun oleh: M Zaky Sai

Jalankan:
    pip install -r requirements.txt
    flask --app app run --debug
"""
import re

from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Data (dictionary / list sebagai pengganti database)
# ---------------------------------------------------------------------------
NAMA_TOKO = "ZakClouth"
MIN_PANJANG = 4

# username yang sudah terdaftar -> data profil
PENGGUNA = {
    "zakysai": {"nama": "M Zaky Sai", "email": "zakysai@mail.com",
                "member": True, "hobi": ["Coding", "Desain", "Fashion"]},
    "andi": {"nama": "Andi Pratama", "email": "andi@mail.com",
             "member": False, "hobi": ["Futsal", "Musik"]},
    "citra": {"nama": "Citra Lestari", "email": "citra@mail.com",
              "member": True, "hobi": []},
}

PRODUK = [
    {"id": 1, "nama": "Kaos Oversize Cloud", "kategori": "kaos", "harga": 89000,
     "stok": 25, "deskripsi": "Kaos oversize katun combed 24s, nyaman dipakai seharian."},
    {"id": 2, "nama": "Hoodie ZakClouth", "kategori": "hoodie", "harga": 185000,
     "stok": 3, "deskripsi": "Hoodie fleece tebal dengan sablon logo ZakClouth di dada."},
    {"id": 3, "nama": "Kemeja Flannel", "kategori": "kemeja", "harga": 150000,
     "stok": 0, "deskripsi": "Kemeja flannel motif kotak, cocok untuk gaya kasual."},
    {"id": 4, "nama": "Celana Cargo", "kategori": "celana", "harga": 175000,
     "stok": 12, "deskripsi": "Celana cargo 6 saku dengan bahan twill yang kuat."},
]


# ---------------------------------------------------------------------------
# Fungsi bantu & filter kustom
# ---------------------------------------------------------------------------
@app.template_filter("rupiah")
def format_rupiah(nilai):
    """18000 -> Rp18.000"""
    return "Rp" + f"{nilai:,}".replace(",", ".")


@app.context_processor
def data_global():
    """Variabel yang otomatis tersedia di semua template."""
    return {"nama_toko": NAMA_TOKO}


def periksa_username(username):
    """
    Validasi + cek ketersediaan username.
    Mengembalikan (valid, tersedia, alasan).
    """
    if len(username) < MIN_PANJANG:
        return False, False, f"Username minimal {MIN_PANJANG} karakter."
    if not re.fullmatch(r"[a-z0-9_]+", username):
        return False, False, "Hanya boleh huruf, angka, dan garis bawah (_)."
    return True, username not in PENGGUNA, ""


# ---------------------------------------------------------------------------
# Route statis (minimal 4 halaman)
# ---------------------------------------------------------------------------
@app.route("/beranda")
@app.route("/")   # didaftarkan pertama -> url_for("index") menghasilkan "/"
def index():
    terlaris = [p for p in PRODUK if p["stok"] > 0][:3]
    return render_template("index.html", terlaris=terlaris)


@app.route("/tentang")
def tentang():
    return render_template("tentang.html")


@app.route("/produk")
def produk():
    # query string opsional: /produk?q=hoodie
    kata = request.args.get("q", "").strip()
    hasil = [p for p in PRODUK if kata.lower() in p["nama"].lower()]
    return render_template("produk.html", produk=hasil, kata=kata)


@app.route("/kontak")
def kontak():
    return render_template("kontak.html")


# ---------------------------------------------------------------------------
# Dynamic route + converter int + abort(404)
# ---------------------------------------------------------------------------
@app.route("/produk/<int:id>")
def detail_produk(id):
    item = next((p for p in PRODUK if p["id"] == id), None)
    if item is None:
        abort(404)
    return render_template("produk_detail.html", p=item)


# ---------------------------------------------------------------------------
# Cek username: /cek/<username>  dan  /cek?u=<username>
# ---------------------------------------------------------------------------
@app.route("/cek")
@app.route("/cek/<username>")
def cek_username(username=None):
    if username is None:                       # versi query string
        username = request.args.get("u", "")
    username = username.strip().lower()

    if username == "":                         # belum ada input -> tampilkan form
        return render_template("cek.html", username="", dicek=False)

    valid, tersedia, alasan = periksa_username(username)
    status = 200 if valid else 400             # tidak valid -> 400 Bad Request
    return render_template("cek.html", username=username, dicek=True,
                           valid=valid, tersedia=tersedia, alasan=alasan), status


@app.route("/user/<username>")
def profil_user(username):
    username = username.strip().lower()
    if len(username) < MIN_PANJANG:
        # terlalu pendek -> arahkan ke halaman cek agar muncul pesan error
        return redirect(url_for("cek_username", username=username))
    data = PENGGUNA.get(username)
    if data is None:
        abort(404)
    return render_template("user.html", username=username, u=data)


@app.route("/daftar-user")
def daftar_user():
    return render_template("daftar_user.html", pengguna=PENGGUNA)


# ---------------------------------------------------------------------------
# redirect: URL lama -> URL baru
# ---------------------------------------------------------------------------
@app.route("/home")
def home_lama():
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Custom halaman error
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def tidak_ditemukan(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
