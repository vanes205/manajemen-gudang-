import streamlit as st
from datetime import date

# PAGE TITLE
st.set_page_config(
    page_title="Sistem Manajemen Gudang",
    page_icon="📦",
    layout="wide"
)

# CUSTOM WARNA
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: linear-gradient(
        135deg,
        #f6d6ff,
        #d8e7ff,
        #ffe3f3
    );
}

/* TITLE */
h1, h2, h3 {
    color: #ff5fa2 !important;
    font-weight: bold;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #f8cce8,
        #cfe5ff
    );
}

/* BUTTON */
.stButton > button {
    width: 100%;
    border-radius: 15px;
    border: none;
    padding: 12px;
    font-weight: bold;
    background: linear-gradient(
        90deg,
        #ff90b3,
        #8fc8ff
    );
    color: white;
}

/* METRIC */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.4);
    padding: 20px;
    border-radius: 18px;
}

</style>
""", unsafe_allow_html=True)

# CLASS NODE
class Node:

    def __init__(
        self,
        nama,
        kode,
        stok=0,
        harga_beli=0,
        harga_jual=0,
        tanggal_masuk="-"
    ):

        self.nama = nama
        self.kode = kode
        self.stok = stok
        self.harga_beli = harga_beli
        self.harga_jual = harga_jual
        self.tanggal_masuk = tanggal_masuk

        self.prev = None
        self.next = None

# CLASS DLL
class DoublyLinkedList:

    def __init__(self):
        self.head = None

    # CARI BARANG
    def cari_barang(self, nama):

        current = self.head

        while current:
            if current.nama.lower() == nama.lower():
                return current
            current = current.next

        return None

    # FUNGSI 1: BARANG MASUK (Otomatis bikin baru atau nambah stok yang ada)
    def proses_barang_masuk(self, nama, kode, jumlah, harga_beli, harga_jual, tanggal):
        
        barang = self.cari_barang(nama)
        
        # Skenario A: Kalau barang sudah terdaftar -> Stok otomatis DITAMBAH (Akumulasi)
        if barang:
            barang.stok += jumlah
            barang.harga_beli = harga_beli
            barang.harga_jual = harga_jual
            barang.tanggal_masuk = tanggal
            return "ditambah"
            
        # Skenario B: Kalau barang benar-benar baru -> Daftarkan jadi gerbong baru (Stok Awal)
        new_node = Node(nama, kode, jumlah, harga_beli, harga_jual, tanggal)
        
        if self.head is None:
            self.head = new_node
            return "baru_dibuat"
            
        current = self.head
        while current.next:
            current = current.next
            
        current.next = new_node
        new_node.prev = current
        return "baru_dibuat"

    # FUNGSI 2: KOREKSI DATA / UPDATE (Menimpa total data karena salah input)
    def koreksi_total_data(self, nama, stok_koreksi, harga_beli_baru, harga_jual_baru, tanggal):
        
        barang = self.cari_barang(nama)
        
        if barang:
            barang.stok = stok_koreksi # Pake = biasa buat menimpa nilai lama
            barang.harga_beli = harga_beli_baru
            barang.harga_jual = harga_jual_baru
            barang.tanggal_masuk = tanggal
            return True
            
        return False

    # BARANG KELUAR
    def barang_keluar(self, nama, jumlah):

        barang = self.cari_barang(nama)

        if barang:

            if jumlah > barang.stok:
                return "stok_kurang"

            barang.stok -= jumlah

            if barang.stok == 0:
                return "habis"

            return "berhasil"

        return "tidak_ada"

    # TAMPILKAN BARANG
    def tampil_barang(self):

        data = []
        current = self.head

        while current:
            data.append({
                "Nama Barang": current.nama,
                "Kode Barang": current.kode,
                "Stok": current.stok,
                "Harga Beli": f"Rp {current.harga_beli:,}",
                "Harga Jual": f"Rp {current.harga_jual:,}",
                "Tanggal Masuk/Update": current.tanggal_masuk
            })
            current = current.next

        return data

    # JUMLAH BARANG
    def jumlah_barang(self):

        current = self.head
        jumlah_jenis = 0
        total_stok = 0

        while current:
            jumlah_jenis += 1
            total_stok += current.stok
            current = current.next

        return jumlah_jenis, total_stok

# SESSION STATE
if "gudang" not in st.session_state:
    st.session_state.gudang = DoublyLinkedList()

if "laporan_masuk" not in st.session_state:
    st.session_state.laporan_masuk = []

if "laporan_keluar" not in st.session_state:
    st.session_state.laporan_keluar = []

gudang = st.session_state.gudang

# TITLE
st.title("📦 Sistem Manajemen Gudang")
st.caption("Menggunakan Doubly Linked List")

# MENU UTAMA
menu = st.sidebar.selectbox(
    "📋 MENU",
    [
        "📥 Barang Masuk",
        "🔄 Koreksi / Update Data",
        "📤 Barang Keluar",
        "🔍 Cari Barang",
        "📦 Semua Barang",
        "📊 Statistik & Laporan"
    ]
)

# 1. MENU BARANG MASUK (Bisa Stok Awal & Bisa Nambah Stok Otomatis)
if menu == "📥 Barang Masuk":

    st.header("📥 Barang Masuk")
    st.caption("Input nama barang. Jika belum ada otomatis jadi stok awal, jika sudah ada otomatis menambah stok lama.")

    nama = st.text_input("📝 Nama Barang")
    kode = st.text_input("🏷️ Kode Barang (Isi bebas jika barang sudah pernah didaftarkan)")
    jumlah = st.number_input("📦 Jumlah Barang Masuk", min_value=1, step=1)
    harga_beli = st.text_input("💰 Harga Beli")
    harga_jual = st.text_input("💸 Harga Jual")
    tanggal_masuk = st.date_input("📅 Tanggal Masuk", value=date.today())

    if st.button("📥 Proses Barang Masuk"):

        if nama.strip() == "" or harga_beli.strip() == "" or harga_jual.strip() == "":
            st.warning("⚠️ Kolom Nama dan Harga wajib diisi!")
        elif not harga_beli.isdigit() or not harga_jual.isdigit():
            st.error("❌ Harga harus berupa angka murni!")
        else:
            # Eksekusi fungsi pintar barang masuk
            hasil = gudang.proses_barang_masuk(
                nama.strip(),
                kode.strip(),
                jumlah,
                int(harga_beli),
                int(harga_jual),
                tanggal_masuk.strftime("%d-%m-%Y")
            )

            # Ambil data kondisi terbaru barang setelah diproses buat info notifikasi
            barang_aktif = gudang.cari_barang(nama.strip())

            if hasil == "baru_dibuat":
                st.session_state.laporan_masuk.append({
                    "Nama Barang": nama.strip(),
                    "Keterangan": "Pendaftaran Stok Awal",
                    "Jumlah": jumlah,
                    "Harga Beli": int(harga_beli),
                    "Harga Jual": int(harga_jual),
                    "Tanggal": tanggal_masuk.strftime("%d-%m-%Y")
                })
                st.success(f"✅ Produk baru '{nama}' berhasil didaftarkan dengan Stok Awal: {jumlah} pcs.")
                
            elif hasil == "ditambah":
                st.session_state.laporan_masuk.append({
                    "Nama Barang": nama.strip(),
                    "Keterangan": "Restock (Tambah Stok)",
                    "Jumlah": jumlah,
                    "Harga Beli": int(harga_beli),
                    "Harga Jual": int(harga_jual),
                    "Tanggal": tanggal_masuk.strftime("%d-%m-%Y")
                })
                st.success(f"📈 Stok '{nama}' berhasil ditambah {jumlah} pcs. Total stok gudang sekarang: {barang_aktif.stok} pcs.")

# 2. MENU KOREKSI DATA (Khusus buat benerin kalau salah input total nilai)
elif menu == "🔄 Koreksi / Update Data":

    st.header("🔄 Koreksi / Update Data (Fitur Salah Input)")
    st.caption("Gunakan menu ini KHUSUS jika ada salah input data. Nilai stok dan harga yang diisi di sini akan MENIMPA total data lama.")

    nama = st.text_input("📝 Masukkan Nama Barang yang Salah Input")
    stok_koreksi = st.number_input("📦 Tulis Total Stok yang Benar Seharusnya", min_value=0, step=1)
    harga_beli_baru = st.text_input("💰 Tulis Harga Beli yang Benar")
    harga_jual_baru = st.text_input("💸 Tulis Harga Jual yang Benar")
    tanggal_koreksi = st.date_input("📅 Tanggal Koreksi", value=date.today())

    if st.button("🔄 Jalankan Koreksi Data"):

        if nama.strip() == "" or harga_beli_baru.strip() == "" or harga_jual_baru.strip() == "":
            st.warning("⚠️ Semua kolom harus diisi untuk mencocokkan data!")
        elif not harga_beli_baru.isdigit() or not harga_jual_baru.isdigit():
            st.error("❌ Format harga harus berupa angka!")
        else:
            hasil = gudang.koreksi_total_data(
                nama.strip(),
                stok_koreksi,
                int(harga_beli_baru),
                int(harga_jual_baru),
                tanggal_koreksi.strftime("%d-%m-%Y")
            )

            if hasil:
                # Catat ke log masuk dengan keterangan Koreksi Salah Input
                st.session_state.laporan_masuk.append({
                    "Nama Barang": nama.strip(),
                    "Keterangan": "Koreksi Salah Input",
                    "Jumlah": stok_koreksi,
                    "Harga Beli": int(harga_beli_baru),
                    "Harga Jual": int(harga_jual_baru),
                    "Tanggal": tanggal_koreksi.strftime("%d-%m-%Y")
                })
                st.success(f"🛠️ Data barang '{nama}' sukses dikoreksi! Total stok akhir sekarang fix diatur menjadi {stok_koreksi} pcs.")
            else:
                st.error("❌ Barang tidak ditemukan! Pastikan ketikan nama produk sudah sesuai.")

# 3. MENU BARANG KELUAR
elif menu == "📤 Barang Keluar":

    st.header("📤 Barang Keluar")

    nama = st.text_input("📝 Nama Barang")
    jumlah = st.number_input("📦 Jumlah Barang Keluar", min_value=1, step=1)
    tanggal_keluar = st.date_input("📅 Tanggal Barang Keluar", value=date.today())

    if st.button("📤 Kurangi Stok"):

        barang_aktif = gudang.cari_barang(nama)
        harga_jual_saat_ini = barang_aktif.harga_jual if barang_aktif else 0

        hasil = gudang.barang_keluar(nama, jumlah)

        if hasil == "berhasil" or hasil == "habis":

            st.session_state.laporan_keluar.append({
                "Nama Barang": nama,
                "Jumlah": jumlah,
                "Harga Jual": harga_jual_saat_ini,
                "Tanggal": tanggal_keluar.strftime("%d-%m-%Y")
            })

            if hasil == "berhasil":
                st.success("✅ Barang berhasil dikeluarkan!")
            else:
                st.warning("⚠️ Stok habis!")

        elif hasil == "stok_kurang":
            st.error("❌ Stok tidak mencukupi!")
        else:
            st.error("❌ Barang tidak ditemukan!")

# 4. MENU CARI BARANG
elif menu == "🔍 Cari Barang":

    st.header("🔍 Cari Barang")
    cari = st.text_input("📝 Nama Barang")

    if st.button("🔍 Cari"):

        barang = gudang.cari_barang(cari)

        if barang:
            st.success("✅ Barang ditemukan!")
            st.write("📦 Nama Barang :", barang.nama)
            st.write("🏷️ Kode Barang :", barang.kode)
            st.write("📊 Stok Saat Ini :", barang.stok)
            st.write("💰 Harga Beli :", f"Rp {barang.harga_beli:,}")
            st.write("💸 Harga Jual :", f"Rp {barang.harga_jual:,}")
            st.write("📅 Update Terakhir :", barang.tanggal_masuk)
        else:
            st.error("❌ Barang tidak ditemukan!")
            
# 5. MENU SEMUA BARANG
elif menu == "📦 Semua Barang":

    st.header("📦 Semua Barang")
    data = gudang.tampil_barang()

    if data:
        st.table(data)
    else:
        st.info("📭 Belum ada data barang.")

# 6. MENU STATISTIK & LAPORAN
elif menu == "📊 Statistik & Laporan":

    st.header("📊 Statistik & Laporan")
    jenis, total = gudang.jumlah_barang()

    # Hitung perputaran dana modal (Abaikan baris koreksi jika dirasa merancukan pembukuan asli)
    total_pengeluaran = 0
    for item in st.session_state.laporan_masuk:
        if item["Keterangan"] != "Koreksi Salah Input":
            total_pengeluaran += item["Jumlah"] * item["Harga Beli"]

    total_pemasukan = 0
    for item in st.session_state.laporan_keluar:
        total_pemasukan += item["Jumlah"] * item["Harga Jual"]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📦 Jumlah Jenis Barang", jenis)
    with col2:
        st.metric("📊 Total Seluruh Stok", total)

    col3, col4 = st.columns(2)
    with col3:
        st.metric("🟥 Pengeluaran Belanja Modal", f"Rp {total_pengeluaran:,}")
    with col4:
        st.metric("🟩 Total Pemasukan Gudang", f"Rp {total_pemasukan:,}")

    st.divider()

    st.subheader("📥 Laporan Log Masuk & Koreksi")
    if st.session_state.laporan_masuk:
        data_masuk_formatted = []
        for x in st.session_state.laporan_masuk:
            data_masuk_formatted.append({
                "Nama Barang": x["Nama Barang"],
                "Keterangan": x["Keterangan"],
                "Jumlah/Stok Akhir": x["Jumlah"],
                "Harga Beli": f"Rp {x['Harga Beli']:,}",
                "Harga Jual": f"Rp {x['Harga Jual']:,}",
                "Tanggal": x["Tanggal"]
            })
        st.table(data_masuk_formatted)
    else:
        st.info("📭 Belum ada rekam data aktivitas masuk.")

    st.divider()

    st.subheader("📤 Laporan Barang Keluar")
    if st.session_state.laporan_keluar:
        data_keluar_formatted = []
        for y in st.session_state.laporan_keluar:
            data_keluar_formatted.append({
                "Nama Barang": y["Nama Barang"],
                "Jumlah": y["Jumlah"],
                "Harga Jual": f"Rp {y['Harga Jual']:,}",
                "Subtotal Pemasukan": f"Rp {y['Jumlah'] * y['Harga Jual']:,}",
                "Tanggal": y["Tanggal"]
            })
        st.table(data_keluar_formatted)
    else:
        st.info("📭 Belum ada laporan barang keluar.")

    st.divider()

    st.warning("⚠️ Reset akan menghapus seluruh data gudang!")
    verifikasi = st.text_input("Ketik 'RESET' untuk konfirmasi")

    if st.button("🔄 Reset Sistem"):
        if verifikasi == "RESET":
            st.session_state.gudang = DoublyLinkedList()
            st.session_state.laporan_masuk = []
            st.session_state.laporan_keluar = []
            st.success("✅ Sistem berhasil direset!")
            st.experimental_rerun()
        else:
            st.error("❌ Verifikasi salah! Ketik RESET.")
