# 💰 War Chest: Financial Survival Tracker

> **A secure, multi-user personal finance application designed to track income, expenses, and estimate financial survival runway.**
> *Built for discipline, engineered for stability.*

![Dashboard Preview](https://via.placeholder.com/800x400?text=Screenshot+Dashboard+WarChest+Lu)
*(Ganti link di atas dengan URL gambar screenshot dashboard War Chest lu yang Neon)*

## 🚀 Overview
**War Chest** bukan sekadar pencatat keuangan biasa. Aplikasi ini dirancang dengan filosofi **"Survival Mode"**, membantu pengguna memvisualisasikan kesehatan finansial mereka secara *real-time*.

Dilengkapi dengan sistem keamanan **Encrypted Authentication**, aplikasi ini mendukung *multi-user* di mana data setiap pengguna terisolasi secara aman. Fitur unggulannya, **Survival Estimation**, menggunakan algoritma berbasis rata-rata pengeluaran harian untuk memprediksi berapa lama saldo saat ini dapat bertahan.

## ✨ Key Features
* **🔒 Secure Authentication:** Sistem Register & Login dengan *password hashing* (Werkzeug) dan manajemen sesi berbasis Token.
* **💀 Survival Mode Logic:** Algoritma cerdas yang menghitung estimasi hari bertahan hidup berdasarkan *burn rate* (rata-rata pengeluaran) harian pengguna.
* **📊 Visual Analytics:** Donut Chart interaktif untuk memvisualisasikan distribusi pengeluaran per kategori (Makan, Transport, Project, dll).
* **📱 Mobile-First UI:** Antarmuka *Cyberpunk Neon* yang responsif dan optimal untuk penggunaan di smartphone.
* **🛡️ Multi-User Isolation:** Database terstruktur yang memisahkan transaksi antar pengguna secara ketat.

## 🛠️ Tech Stack
* **Backend:** Python (Flask), SQLAlchemy (ORM), Werkzeug (Security)
* **Database:** SQLite (Relational DB)
* **Frontend:** HTML5, CSS3 (Glassmorphism UI), JavaScript (Vanilla Fetch API)
* **Visualization:** Chart.js

## 📦 Installation & Setup

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/rifki-ardhika-putra7/war-chest-finance.git](https://github.com/rifki-ardhika-putra7/war-chest-finance.git)
    cd war-chest-finance
    ```

2.  **Install Dependencies**
    ```bash
    pip install flask flask-sqlalchemy flask-cors werkzeug
    ```

3.  **Run Application**
    ```bash
    python app.py
    ```
    Akses aplikasi di: `http://localhost:5001`

## 🧪 Usage Guide
1.  **Register:** Buat akun baru di halaman awal.
2.  **Input Transaksi:** Masukkan pemasukan (Income) atau pengeluaran (Expense).
3.  **Monitor:** Pantau "Saldo Perang" dan indikator "Survival Estimation" di dashboard.

## 🤝 Contact
Dibuat oleh **Kay** - *Informatics Engineering Student & Full Stack Developer*.
[LinkedIn](Link LinkedIn Lu) | [rfkikun@gmail.com](Email Lu)
