import streamlit as st
from datetime import date
import pandas as pd

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
        #f8d7ff,
        #dbe8ff,
        #ffe3f1
    );
}

/* TITLE */
h1, h2, h3 {
    color: #ff5f9e !important;
    font-weight: bold;
}

/* TEXT */
p, label, div {
    color: #4b4b4b;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #f7c8e9,
        #cde4ff
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
        #ff8eb5,
        #8fc7ff
    );
    color: white;
    transition: 0.3s;
    box-shadow: 0 4px 12px rgba(255, 182, 193, 0.4);
}

.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(
        90deg,
        #ff75a6,
        #73b8ff
    );
}

/* INPUT */
input, textarea {
    border-radius: 12px !important;
    border: 1px solid #ffd3ea !important;
}

/* METRIC */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.4);
    padding: 20px;
    border-radius: 18px;
    backdrop-filter: blur(10px);
}

/* DATAFRAME */
div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.35);
    border-radius: 15px;
    padding: 10px;
}

/* ALERT */
.stAlert {
    border-radius: 15px;
}

/* CONTAINER */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# =========================
# CLASS NODE
# =========================
class Node:
    def __init__(self, nama, kode, stok, tanggal_masuk):
        self.nama = nama
        self.kode = kode
        self.stok = stok
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
    def tambah_barang(self, nama, kode, stok, tanggal):

        current = self.head

        while current:
            if current.nama.lower() == nama.lower():
                return False

            current = current.next

        new_node = Node(
            nama,
            kode,
            stok,
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
    def barang_masuk(self, nama, jumlah):

        barang = self.cari_barang(nama)

        if barang:
            barang.stok += jumlah
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

gudang = st.session_state.gudang

# =========================
# TITLE
# =========================
st.title("📦 Sistem Manajemen Gudang")
st.caption("Manajemen stok barang menggunakan Doubly Linked List")

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox(
    "📋 MENU UTAMA",
    [
        "➕ Tambah Barang",
        "📥 Barang Masuk",
        "📤 Barang Keluar",
        "🔍 Cari Barang",
        "✏️ Update Stok",
        "📦 Semua Barang",
        "📊 Statistik Gudang"
    ]
)

# =========================
# TAMBAH BARANG
# =========================
if menu == "➕ Tambah Barang":

    st.header("➕ Tambah Barang")

    col1, col2 = st.columns(2)

    with col1:
        nama = st.text_input("📝 Nama Barang")
        kode = st.text_input("🏷️ Kode Barang")

    with col2:
        stok = st.number_input(
            "📦 Jumlah Stok",
            min_value=1
        )

        tanggal = st.date_input(
            "📅 Tanggal Masuk",
            value=date.today()
        )

    if st.button("➕ Tambah Barang"):

        if nama.strip() == "" or kode.strip() == "":
            st.warning("⚠️ Input tidak boleh kosong!")

        else:

            hasil = gudang.tambah_barang(
                nama,
                kode,
                stok,
                tanggal.strftime("%d-%m-%Y")
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
        "📦 Jumlah Tambahan",
        min_value=1
    )

    if st.button("📥 Tambah Stok"):

        if gudang.barang_masuk(nama, jumlah):
            st.success("✅ Stok berhasil ditambahkan!")

        else:
            st.error("❌ Barang tidak ditemukan!")

# =========================
# BARANG KELUAR
# =========================
elif menu == "📤 Barang Keluar":

    st.header("📤 Barang Keluar")

    nama = st.text_input("📝 Nama Barang")

    jumlah = st.number_input(
        "📦 Jumlah Keluar",
        min_value=1
    )

    tanggal_keluar = st.date_input(
        "📅 Tanggal Keluar",
        value=date.today()
    )

    if st.button("📤 Kurangi Stok"):

        hasil = gudang.barang_keluar(
            nama,
            jumlah
        )

        if hasil == "berhasil":

            st.success("✅ Barang berhasil dikeluarkan!")

            st.info(
                f"📅 Tanggal Keluar : "
                f"{tanggal_keluar.strftime('%d-%m-%Y')}"
            )

        elif hasil == "habis":
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
            st.write("📊 Stok Barang :", barang.stok)
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

    if st.button("✏️ Update Stok"):

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

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.info("📭 Belum ada data barang.")

# =========================
# STATISTIK
# =========================
elif menu == "📊 Statistik Gudang":

    st.header("📊 Statistik Gudang")

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

    if st.button("🔄 Reset Sistem"):

        st.session_state.gudang = DoublyLinkedList()

        st.success("✅ Sistem berhasil direset!")

        st.rerun()
