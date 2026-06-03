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

    # TAMBAH BARANG BARU (Digunakan sebagai pendaftaran Stok Awal)
    def tambah_barang_baru(self, nama, kode, stok, harga_beli, harga_jual, tanggal):

        current = self.head

        # Validasi ganda: Pastikan nama atau kode belum ada di gudang
        while current:
            if current.nama.lower() == nama.lower() or current.kode.lower() == kode.lower():
                return False
            current = current.next

        new_node = Node(nama, kode, stok, harga_beli, harga_jual, tanggal)

        if self.head is None:
            self.head = new_node
            return True

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node
        new_node.prev = current

        return True

    # CARI BARANG
    def cari_barang(self, nama):

        current = self.head

        while current:
            if current.nama.lower() == nama.lower():
                return current
            current = current.next

        return None

    # UPDATE BARANG (Mengubah stok dan harga barang yang sudah ada)
    def update_barang(self, nama, stok_baru, harga_beli_baru, harga_jual_saat_ini, tanggal):
        
        barang = self.cari_barang(nama)
        
        if barang:
            barang.stok = stok_baru
            barang.harga_beli = harga_beli_baru
            barang.harga_jual = harga_jual_saat_ini
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
                "Tanggal Update": current.tanggal_masuk
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

# MENU (Tambah Barang Dihapus, diganti Menu Update)
menu = st.sidebar.selectbox(
    "📋 MENU",
    [
        "📥 Barang Masuk (Stok Awal)",
        "🔄 Update Data Barang",
        "📤 Barang Keluar",
        "🔍 Cari Barang",
        "📦 Semua Barang",
        "📊 Statistik & Laporan"
    ]
)

# 1. MENU BARANG MASUK (Mendaftarkan Barang + Stok Awal)
if menu == "📥 Barang Masuk (Stok Awal)":

    st.header("📥 Barang Masuk (Pendaftaran Stok Awal)")
    st.caption("Gunakan menu ini untuk mendaftarkan produk baru yang belum pernah tercatat di gudang.")

    nama = st.text_input("📝 Nama Barang Baru")
    kode = st.text_input("🏷️ Kode Barang")
    stok_awal = st.number_input("📦 Jumlah Stok Awal", min_value=1, step=1)
    harga_beli = st.text_input("💰 Harga Beli Awal")
    harga_jual = st.text_input("💸 Harga Jual Awal")
    tanggal_masuk = st.date_input("📅 Tanggal Masuk", value=date.today())

    if st.button("📥 Daftarkan Barang & Stok"):

        if nama.strip() == "" or kode.strip() == "" or harga_beli.strip() == "" or harga_jual.strip() == "":
            st.warning("⚠️ Semua input wajib diisi!")
        elif not harga_beli.isdigit() or not harga_jual.isdigit():
            st.error("❌ Harga beli dan harga jual harus berupa angka murni!")
        else:
            hasil = gudang.tambah_barang_baru(
                nama.strip(),
                kode.strip(),
                stok_awal,
                int(harga_beli),
                int(harga_jual),
                tanggal_masuk.strftime("%d-%m-%Y")
            )

            if hasil:
                # Catat ke dalam laporan masuk sebagai stok awal
                st.session_state.laporan_masuk.append({
                    "Nama Barang": nama.strip(),
                    "Keterangan": "Stok Awal Baru",
                    "Jumlah": stok_awal,
                    "Harga Beli": int(harga_beli),
                    "Harga Jual": int(harga_jual),
                    "Tanggal": tanggal_masuk.strftime("%d-%m-%Y")
                })
                st.success(f"✅ Produk '{nama}' dengan stok awal {stok_awal} berhasil didaftarkan!")
            else:
                st.error("❌ Gagal! Nama barang atau Kode barang sudah ada di gudang. Silakan gunakan menu 'Update Data Barang'.")

# 2. MENU UPDATE BARANG (Mengubah Stok dan Harga barang yang sudah ada)
elif menu == "🔄 Update Data Barang":

    st.header("🔄 Update Data Barang")
    st.caption("Gunakan menu ini untuk mengubah jumlah stok akhir maupun memperbarui harga barang.")

    nama = st.text_input("📝 Masukkan Nama Barang yang Ingin Diupdate")
    stok_baru = st.number_input("📦 Ubah Total Stok Menjadi", min_value=0, step=1)
    harga_beli_baru = st.text_input("💰 Update Harga Beli Baru")
    harga_jual_baru = st.text_input("💸 Update Harga Jual Baru")
    tanggal_update = st.date_input("📅 Tanggal Update", value=date.today())

    if st.button("🔄 Perbarui Data Barang"):

        if nama.strip() == "" or harga_beli_baru.strip() == "" or harga_jual_baru.strip() == "":
            st.warning("⚠️ Semua kolom harus diisi untuk proses update!")
        elif not harga_beli_baru.isdigit() or not harga_jual_baru.isdigit():
            st.error("❌ Format harga harus berupa angka murni!")
        else:
            # Jalankan pencarian dan update data pada Linked List
            hasil = gudang.update_barang(
                nama.strip(),
                stok_baru,
                int(harga_beli_baru),
                int(harga_jual_baru),
                tanggal_update.strftime("%d-%m-%Y")
            )

            if hasil:
                # Catat ke log laporan masuk sebagai aktivitas penyesuaian/update data
                st.session_state.laporan_masuk.append({
                    "Nama Barang": nama.strip(),
                    "Keterangan": "Update Data & Stok",
                    "Jumlah": stok_baru,
                    "Harga Beli": int(harga_beli_baru),
                    "Harga Jual": int(harga_jual_baru),
                    "Tanggal": tanggal_update.strftime("%d-%m-%Y")
                })
                st.success(f"✅ Data produk '{nama}' berhasil diperbarui!")
            else:
                st.error("❌ Barang tidak ditemukan! Pastikan nama yang diketik sesuai dengan yang ada di gudang.")

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

    # Hitung total pengeluaran belanja modal gudang
    total_pengeluaran = 0
    for item in st.session_state.laporan_masuk:
        total_pengeluaran += item["Jumlah"] * item["Harga Beli"]

    # Hitung total pemasukan omzet
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
        st.metric("🟥 Pengeluaran Kulakan/Awal", f"Rp {total_pengeluaran:,}")
    with col4:
        st.metric("🟩 Total Pemasukan Gudang", f"Rp {total_pemasukan:,}")

    st.divider()

    st.subheader("📥 Laporan Log Masuk & Update")
    if st.session_state.laporan_masuk:
        data_masuk_formatted = []
        for x in st.session_state.laporan_masuk:
            data_masuk_formatted.append({
                "Nama Barang": x["Nama Barang"],
                "Keterangan": x["Keterangan"],
                "Jumlah": x["Jumlah"],
                "Harga Beli": f"Rp {x['Harga Beli']:,}",
                "Harga Jual": f"Rp {x['Harga Jual']:,}",
                "Subtotal Nilai": f"Rp {x['Jumlah'] * x['Harga Beli']:,}",
                "Tanggal": x["Tanggal"]
            })
        st.table(data_masuk_formatted)
    else:
        st.info("📭 Belum ada rekam data masuk.")

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
            st.rerun()
        else:
            st.error("❌ Verifikasi salah! Ketik RESET.")
