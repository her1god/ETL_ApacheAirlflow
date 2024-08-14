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

1. **Unduh dataset**: Tambahkan bagian di README yang menjelaskan cara mengunduh dataset. Anda dapat menyertakan link ke Google Drive atau tempat penyimpanan lainnya, serta memberikan instruksi tentang cara mengunduh dan menempatkan dataset di dalam proyek.

    ```markdown
    ## Unduh Dataset

    Anda dapat mengunduh dataset untuk proyek ini dari tautan berikut:

    [Download Dataset](https://drive.google.com/file/d/1crLu-zsVLiWEdjsL9JporpKpiDo69wGk/view?usp=sharing)

    Setelah mengunduh dataset, letakkan file-file tersebut di dalam folder `data`.
    ```

2. **Clone Repository:**

    ```bash
    git clone https://github.com/her1god/ETL_ApacheAirlflow.git
    ```

3. **Membuat file .env**: Berikan instruksi kepada pengguna tentang bagaimana cara membuat file `.env` dan mengisi variabel lingkungan yang diperlukan untuk koneksi ke database PostgreSQL. Anda juga dapat memberikan contoh isi file `.env`.

    ```markdown
    ## Konfigurasi .env

    Untuk menjalankan proyek ini, Anda perlu membuat file `.env` di dalam folder `env` dan mengisi variabel lingkungan berikut:

    ```
    POSTGRES_USER=your_username

    POSTGRES_PASSWORD=your_password

    POSTGRES_HOST=your_host

    POSTGRES_PORT=your_port

    POSTGRES_DB=your_database

    ```

    Pastikan untuk mengganti `your_username`, `your_password`, `your_host`, `your_port`, dan `your_database` dengan informasi koneksi PostgreSQL Anda.
    ```

4. **Buat dan Aktifkan Lingkungan Virtual:**

    ```markdown
    python3 -m venv venv
    source venv/bin/activate
    export AIRFLOW_HOME=~/nama_folder
    cek apakah sudah berada difolder sama dengan > airflow info
    ```

5. **Instal Dependensi:**

    ```bash
    pip install -r requirements.txt
    ```

6. **Jalankan Apache Airflow:**

    Pastikan Apache Airflow telah terinstal dan dikonfigurasi di sistem Anda. Kemudian, jalankan:

    ```markdown
    buka airflow.cfg, cari sql_alchemy_conn lalu isi dengan postgresql+psycopg2://username:password@localhost/database
    dan juga cari executor lalu ubah menjadi executor = LocalExecutor.
    airflow users create --username admin --firstname FIRSTNAME --lastname LASTNAME --role Admin --email admin@example.com --password admin
    airflow db migrate
    airflow webserver -p 8080
    airflow scheduler
    ```

7. **Tambah dan Jalankan DAG:**

    Tambahkan DAG Anda ke direktori `dags/` Airflow dan pantau melalui antarmuka web Airflow di `http://localhost:8080`.

## Penggunaan

Setelah Anda memulai Airflow, Anda dapat menjalankan DAG Anda secara manual atau mengatur jadwal untuk menjalankannya secara otomatis. Pantau status DAG dan tugas melalui antarmuka web Airflow.

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan buat pull request atau buka masalah jika Anda menemukan bug.

## Lisensi

Proyek ini dilisensikan di bawah -

---
