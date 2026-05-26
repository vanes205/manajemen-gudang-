import streamlit as st
from datetime import date

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Sistem Manajemen Gudang",
    page_icon="📦",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
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

/* INPUT */
input {
    border-radius: 12px !important;
}

/* METRIC */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.4);
    padding: 20px;
    border-radius: 18px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# CLASS NODE
# =========================
class Node:

    def __init__(
        self,
        nama,
        kode,
        stok,
        harga_beli,
        harga_jual,
        tanggal_masuk
    ):

        self.nama = nama
        self.kode = kode
        self.stok = stok
        self.harga_beli = harga_beli
        self.harga_jual = harga_jual
        self.tanggal_masuk = tanggal_masuk

        self.prev = None
        self.next = None

# =========================
# CLASS DLL
# =========================
class DoublyLinkedList:

    def __init__(self):
        self.head = None

    # TAMBAH BARANG
    def tambah_barang(
        self,
        nama,
        kode,
        stok,
        harga_beli,
        harga_jual,
        tanggal
    ):

        current = self.head

        while current:

            if current.nama.lower() == nama.lower():
                return False

            current = current.next

        new_node = Node(
            nama,
            kode,
            stok,
            harga_beli,
            harga_jual,
            tanggal
        )

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

    # BARANG MASUK
    def barang_masuk(self, nama, jumlah, tanggal):

        barang = self.cari_barang(nama)

        if barang:

            barang.stok += jumlah
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
                self.hapus_barang(nama)
                return "habis"

            return "berhasil"

        return "tidak_ada"

    # HAPUS BARANG
    def hapus_barang(self, nama):

        current = self.head

        while current:

            if current.nama.lower() == nama.lower():

                if current == self.head:

                    self.head = current.next

                    if self.head:
                        self.head.prev = None

                else:

                    if current.prev:
                        current.prev.next = current.next

                    if current.next:
                        current.next.prev = current.prev

                return True

            current = current.next

        return False

    # UPDATE STOK
    def update_stok(self, nama, stok_baru):

        barang = self.cari_barang(nama)

        if barang:

            barang.stok = stok_baru
            return True

        return False

    # TAMPILKAN BARANG
    def tampil_barang(self):

        data = []

        current = self.head

        while current:

            data.append({
                "Nama Barang": current.nama,
                "Kode Barang": current.kode,
                "Stok": current.stok,
                "Harga Beli": f"Rp {current.harga_beli}",
                "Harga Jual": f"Rp {current.harga_jual}",
                "Tanggal Masuk": current.tanggal_masuk
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

# =========================
# SESSION STATE
# =========================
if "gudang" not in st.session_state:
    st.session_state.gudang = DoublyLinkedList()

if "laporan_masuk" not in st.session_state:
    st.session_state.laporan_masuk = []

if "laporan_keluar" not in st.session_state:
    st.session_state.laporan_keluar = []

gudang = st.session_state.gudang

# =========================
# TITLE
# =========================
st.title("📦 Sistem Manajemen Gudang")
st.caption("Menggunakan Doubly Linked List")

# =========================
# MENU
# =========================
menu = st.sidebar.selectbox(
    "📋 MENU",
    [
        "➕ Tambah Barang",
        "📥 Barang Masuk",
        "📤 Barang Keluar",
        "🔍 Cari Barang",
        "✏️ Update Stok",
        "📦 Semua Barang",
        "📊 Statistik & Laporan"
    ]
)

# =========================
# TAMBAH BARANG
# =========================
if menu == "➕ Tambah Barang":

    st.header("➕ Tambah Barang")

    nama = st.text_input("📝 Nama Barang")

    kode = st.text_input("🏷️ Kode Barang")

    harga_beli = st.text_input(
        "💰 Harga Beli"
    )

    harga_jual = st.text_input(
        "💸 Harga Jual"
    )

    if st.button("➕ Tambah Barang"):

        if (
            nama.strip() == ""
            or kode.strip() == ""
            or harga_beli.strip() == ""
            or harga_jual.strip() == ""
        ):

            st.warning("⚠️ Semua input harus diisi!")

        elif (
            not harga_beli.isdigit()
            or not harga_jual.isdigit()
        ):

            st.error("❌ Harga harus berupa angka!")

        else:

            hasil = gudang.tambah_barang(
                nama,
                kode,
                0,
                int(harga_beli),
                int(harga_jual),
                "-"
            )

            if hasil:
                st.success("✅ Barang berhasil ditambahkan!")

            else:
                st.warning("⚠️ Barang sudah ada!")

# =========================
# BARANG MASUK
# =========================
elif menu == "📥 Barang Masuk":

    st.header("📥 Barang Masuk")

    nama = st.text_input("📝 Nama Barang")

    jumlah = st.number_input(
        "📦 Jumlah Barang Masuk",
        min_value=1
    )

    tanggal_masuk = st.date_input(
        "📅 Tanggal Barang Masuk",
        value=date.today()
    )

    if st.button("📥 Tambah Stok"):

        hasil = gudang.barang_masuk(
            nama,
            jumlah,
            tanggal_masuk.strftime("%d-%m-%Y")
        )

        if hasil:

            st.session_state.laporan_masuk.append({
                "Nama Barang": nama,
                "Jumlah": jumlah,
                "Tanggal": tanggal_masuk.strftime("%d-%m-%Y")
            })

            st.success("✅ Barang masuk berhasil ditambahkan!")

        else:
            st.error("❌ Barang tidak ditemukan!")

# =========================
# BARANG KELUAR
# =========================
elif menu == "📤 Barang Keluar":

    st.header("📤 Barang Keluar")

    nama = st.text_input("📝 Nama Barang")

    jumlah = st.number_input(
        "📦 Jumlah Barang Keluar",
        min_value=1
    )

    tanggal_keluar = st.date_input(
        "📅 Tanggal Barang Keluar",
        value=date.today()
    )

    if st.button("📤 Kurangi Stok"):

        hasil = gudang.barang_keluar(
            nama,
            jumlah
        )

        if hasil == "berhasil":

            st.session_state.laporan_keluar.append({
                "Nama Barang": nama,
                "Jumlah": jumlah,
                "Tanggal": tanggal_keluar.strftime("%d-%m-%Y")
            })

            st.success("✅ Barang berhasil dikeluarkan!")

        elif hasil == "habis":

            st.session_state.laporan_keluar.append({
                "Nama Barang": nama,
                "Jumlah": jumlah,
                "Tanggal": tanggal_keluar.strftime("%d-%m-%Y")
            })

            st.warning("⚠️ Stok habis! Barang dihapus.")

        elif hasil == "stok_kurang":
            st.error("❌ Stok tidak mencukupi!")

        else:
            st.error("❌ Barang tidak ditemukan!")

# =========================
# CARI BARANG
# =========================
elif menu == "🔍 Cari Barang":

    st.header("🔍 Cari Barang")

    cari = st.text_input("📝 Nama Barang")

    if st.button("🔍 Cari"):

        barang = gudang.cari_barang(cari)

        if barang:

            st.success("✅ Barang ditemukan!")

            st.write("📦 Nama Barang :", barang.nama)
            st.write("🏷️ Kode Barang :", barang.kode)
            st.write("📊 Stok :", barang.stok)
            st.write("💰 Harga Beli :", barang.harga_beli)
            st.write("💸 Harga Jual :", barang.harga_jual)
            st.write("📅 Tanggal Masuk :", barang.tanggal_masuk)

        else:
            st.error("❌ Barang tidak ditemukan!")

# =========================
# UPDATE STOK
# =========================
elif menu == "✏️ Update Stok":

    st.header("✏️ Update Stok")

    nama = st.text_input("📝 Nama Barang")

    stok_baru = st.number_input(
        "📦 Stok Baru",
        min_value=0
    )

    if st.button("✏️ Update"):

        if gudang.update_stok(nama, stok_baru):

            st.success("✅ Stok berhasil diupdate!")

        else:
            st.error("❌ Barang tidak ditemukan!")

# =========================
# SEMUA BARANG
# =========================
elif menu == "📦 Semua Barang":

    st.header("📦 Semua Barang")

    data = gudang.tampil_barang()

    if data:
        st.table(data)

    else:
        st.info("📭 Belum ada data barang.")

# =========================
# STATISTIK & LAPORAN
# =========================
elif menu == "📊 Statistik & Laporan":

    st.header("📊 Statistik & Laporan")

    jenis, total = gudang.jumlah_barang()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📦 Jumlah Jenis Barang",
            jenis
        )

    with col2:
        st.metric(
            "📊 Total Seluruh Stok",
            total
        )

    st.divider()

    st.subheader("📥 Laporan Barang Masuk")

    if st.session_state.laporan_masuk:
        st.table(st.session_state.laporan_masuk)

    else:
        st.info("📭 Belum ada laporan barang masuk.")

    st.divider()

    st.subheader("📤 Laporan Barang Keluar")

    if st.session_state.laporan_keluar:
        st.table(st.session_state.laporan_keluar)

    else:
        st.info("📭 Belum ada laporan barang keluar.")

    st.divider()

    st.warning("⚠️ Reset akan menghapus seluruh data gudang!")

    verifikasi = st.text_input(
        "Ketik 'RESET' untuk konfirmasi"
    )

    if st.button("🔄 Reset Sistem"):

        if verifikasi == "RESET":

            st.session_state.gudang = DoublyLinkedList()
            st.session_state.laporan_masuk = []
            st.session_state.laporan_keluar = []

            st.success("✅ Sistem berhasil direset!")

            st.rerun()

        else:
            st.error("❌ Verifikasi salah! Ketik RESET.")
