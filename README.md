# Simple Task Project Tracker

Aplikasi manajemen tugas (Task/Project Tracker) full-stack sederhana yang dibangun menggunakan FastAPI (Python), Vue 3 (Composition API), dan database PostgreSQL.

---

## Fitur Utama

- **Task List Display**: Menampilkan seluruh daftar tugas secara real-time dari database.
- **Create Task Form**: Menambahkan tugas baru secara dinamis tanpa reload halaman.
- **Status Toggler**: Mengubah status pengerjaan tugas (`Todo` -> `In Progress` -> `Done`).
- **Delete Task**: Menghapus data tugas dari database dengan dialog konfirmasi.
- **Feedback UI/UX**: Loading state, penanganan error jaringan, dan proteksi tombol submit.

---

## Teknologi dan Versi Tools

| Komponen | Tool / Framework | Versi Rekomendasi |
| :--- | :--- | :--- |
| **Backend Runtime** | Python | 3.11+ |
| **Backend Framework** | FastAPI | >= 0.110.0 |
| **ASGI Server** | Uvicorn | >= 0.28.0 |
| **ORM & Driver** | SQLAlchemy / psycopg | 2.0+ / 3.1+ |
| **Database** | PostgreSQL | 16-alpine |
| **Frontend Runtime** | Node.js | 20+ (LTS) |
| **Frontend Framework** | Vue.js | 3.5+ (Composition API) |
| **Build Tool** | Vite | 8.3+ |
| **Styling** | Tailwind CSS | 4.3+ |
| **HTTP Client** | Axios | 1.20+ |
| **Containerization** | Docker & Docker Compose | Docker v24+ / Compose v2+ |

---

## Cara Menjalankan Aplikasi

Pilih salah satu cara di bawah: menggunakan **Docker** (direkomendasikan) atau **Lokal**.

### Opsi 1: Menjalankan dengan Docker (Direkomendasikan)

Pastikan Docker Desktop sudah aktif di komputer Anda.

1. **Clone repository dan masuk ke direktori:**
   ```bash
   git clone <url-repository>
   cd "Simple Task Project Tracker"
   ```

2. **Siapkan file environment:**
   Salin file contoh konfigurasi di root folder:
   ```bash
   cp .env.example .env
   ```
   *(Opsional: sesuaikan user, password, dan port database di file `.env` jika diperlukan).*

3. **Jalankan seluruh service:**
   ```bash
   docker compose up --build
   ```

4. **Akses aplikasi:**
   - **Frontend (Vue 3)**: [http://localhost:5173](http://localhost:5173)
   - **Backend API & Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **PostgreSQL**: Port `5433`

Untuk mematikan container:
```bash
docker compose down
```

---

### Opsi 2: Menjalankan Secara Lokal (Tanpa Docker)

#### Syarat
- Python 3.11+ dan Node.js 20+ sudah terpasang.
- Service PostgreSQL aktif di komputer Anda (misal pada port `5433` atau `5432`). Buat database bernama `simple_task_project_tracker`.

#### 1. Setup Backend (FastAPI)
```bash
cd backend

# Buat dan aktifkan virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1


# Install dependensi
pip install -r requirements.txt

# Buat file .env dari template
cp .env.example .env
# Edit file .env dan sesuaikan URL koneksi PostgreSQL Anda

# Jalankan server FastAPI
uvicorn app.main:app --reload --port 8000
```
API backend akan aktif di [http://localhost:8000](http://localhost:8000).

#### 2. Setup Frontend (Vue 3)
Buka terminal baru:
```bash
cd frontend

# Install dependensi Node
npm install

# Buat file .env dari template
cp .env.example .env

# Jalankan dev server Vite
npm run dev
```
Frontend akan aktif di [http://localhost:5173](http://localhost:5173).

---