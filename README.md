---

# Proyek ETL dengan Apache Airflow

![Gambar Proyek ETL](https://github.com/her1god/ETL_ApacheAirlflow/blob/main/ETL%20Books%20Reviews%20in%20Website%20GoodReads.png) <!-- Ganti URL dengan URL gambar Anda -->

## Deskripsi

Ini adalah proyek ETL (Extract, Transform, Load) yang menggunakan Apache Airflow untuk mengelola alur kerja ETL. Data yang digunakan berasal dari dataset yang diambil dari website Goodreads. Proyek ini menyertakan ekstraksi data, transformasi data, dan pemuatan data ke dalam database PostgreSQL.

## Fitur Utama

- **Ekstraksi Data:** Mengambil data buku, ulasan buku, dan detail buku dari Goodreads.
- **Transformasi Data:** Membersihkan dan memformat data, termasuk konversi tanggal, penghapusan nilai yang tidak diinginkan, dan perubahan tipe data.
- **Pemuatan Data:** Menyimpan data yang sudah diproses ke dalam file CSV dan juga ke database PostgreSQL.
- **Manajemen Alur Kerja:** Dikelola menggunakan Apache Airflow untuk memastikan bahwa setiap langkah ETL dilakukan secara teratur dan dapat dipantau.

## Struktur Proyek

- `dags/`: Berisi definisi DAG untuk Apache Airflow.
- `extract.py`: Skrip untuk mengekstraksi data.
- `transform.py`: Skrip untuk mentransformasi data.
- `load.py`: Skrip untuk memuat data ke dalam file CSV dan PostgreSQL.
- `requirements.txt`: Daftar pustaka Python yang diperlukan.

## Instalasi

1. **Clone Repository:**

    ```bash
    git clone https://github.com/username/repository.git
    ```

2. **Buat dan Aktifkan Lingkungan Virtual:**

    ```bash
    python3 -m venv airflow_f1
    source airflow_f1/bin/activate
    ```

3. **Instal Dependensi:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Jalankan Apache Airflow:**

    Pastikan Apache Airflow telah terinstal dan dikonfigurasi di sistem Anda. Kemudian, jalankan:

    ```bash
    airflow db init
    airflow webserver -p 8080
    airflow scheduler
    ```

5. **Tambah dan Jalankan DAG:**

    Tambahkan DAG Anda ke direktori `dags/` Airflow dan pantau melalui antarmuka web Airflow di `http://localhost:8080`.

## Penggunaan

Setelah Anda memulai Airflow, Anda dapat menjalankan DAG Anda secara manual atau mengatur jadwal untuk menjalankannya secara otomatis. Pantau status DAG dan tugas melalui antarmuka web Airflow.

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan buat pull request atau buka masalah jika Anda menemukan bug.

## Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE).

---

Silakan sesuaikan URL gambar dan informasi lainnya sesuai dengan kebutuhan Anda!
