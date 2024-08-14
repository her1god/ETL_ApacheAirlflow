from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import os
import pandas as pd
from extract import extract_book_details, extract_book_reviews, extract_books
from transform import transform_book_details, transform_book_reviews, transform_books
from load import load_data_to_csv, load_data_to_postgres

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'start_date': datetime(2024, 8, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

# DAG definition
dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='An ETL pipeline for processing book data',
    schedule_interval='@daily',
    catchup=False,
)

# Task untuk ekstraksi data
def extract_data():
    try:
        book_details_df = extract_book_details()
        book_reviews_df = extract_book_reviews()
        books_df = extract_books()

        # Simpan data ke Variable Airflow
        Variable.set("book_details_data", book_details_df.to_json())
        Variable.set("book_reviews_data", book_reviews_df.to_json())
        Variable.set("books_data", books_df.to_json())

        return "Data extraction completed successfully"
    except Exception as e:
        raise Exception(f"Error extracting data: {str(e)}")

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

# Task untuk transformasi data
def transform_data_wrapper(**kwargs):
    try:
        book_details_json = Variable.get("book_details_data")
        book_reviews_json = Variable.get("book_reviews_data")
        books_json = Variable.get("books_data")

        book_details_df = pd.read_json(book_details_json)
        book_reviews_df = pd.read_json(book_reviews_json)
        books_df = pd.read_json(books_json)

        transformed_book_details_df = transform_book_details(book_details_df.copy())
        transformed_book_reviews_df = transform_book_reviews(book_reviews_df.copy())
        transformed_books_df = transform_books(books_df.copy())

        # Menggabungkan DataFrame berdasarkan kolom 'book_id'
        merged_df = pd.merge(transformed_books_df, transformed_book_details_df, on='book_id', how='inner')
        merged_df = pd.merge(merged_df, transformed_book_reviews_df, on='book_id', how='inner')

        # Mengonversi tipe data kembali ke integer setelah penggabungan
        columns_to_int = ['book_id', 'num_pages', 'likes_on_review', 'reviewer_total_reviews', 'reviewer_followers', 'review_rating', 'reviewer_id']
        for col in columns_to_int:
            if col in merged_df.columns:
                merged_df[col] = merged_df[col].fillna(0).astype(int)

        # Menghapus kolom 'Unnamed: 0' jika ada
        if 'Unnamed: 0' in merged_df.columns:
            merged_df = merged_df.drop(columns=['Unnamed: 0'])

        # Buat DataFrame clean_merged_books, clean_books_data, dan clean_books_reviews
        clean_merged_books = merged_df.copy()
        clean_books_data = merged_df[['book_id', 'title', 'total_books', 'total_votes', 'cover_image_uri', 'book_title', 'book_details', 'format', 'publication_info', 'num_pages', 'genres', 'num_ratings', 'num_reviews', 'average_rating', 'rating_distribution']].drop_duplicates().reset_index(drop=True)
        clean_books_reviews = merged_df[['book_id', 'reviewer_id', 'reviewer_name', 'likes_on_review', 'review_content', 'reviewer_followers', 'reviewer_total_reviews', 'review_date', 'review_rating']]

        # Lokasi untuk menyimpan data bersih
        clean_data_dir = 'data_clean'
        if not os.path.exists(clean_data_dir):
            os.makedirs(clean_data_dir)

        # Simpan DataFrame ke Variable Airflow
        Variable.set("clean_merged_books_data", clean_merged_books.to_json())
        Variable.set("clean_books_data", clean_books_data.to_json())
        Variable.set("clean_books_reviews_data", clean_books_reviews.to_json())

        return "Data transformation completed successfully"
    except Exception as e:
        raise Exception(f"Error transforming data: {str(e)}")

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data_wrapper,
    provide_context=True,
    dag=dag,
)

# Task untuk memuat data ke CSV dan PostgreSQL
def load_data_wrapper(**kwargs):
    try:
        clean_merged_books_json = Variable.get("clean_merged_books_data")
        clean_books_data_json = Variable.get("clean_books_data")
        clean_books_reviews_json = Variable.get("clean_books_reviews_data")

        clean_merged_books = pd.read_json(clean_merged_books_json)
        clean_books_data = pd.read_json(clean_books_data_json)
        clean_books_reviews = pd.read_json(clean_books_reviews_json)

        # Simpan ke CSV
        clean_data_dir = 'data_clean'
        if not os.path.exists(clean_data_dir):
            os.makedirs(clean_data_dir)
        load_data_to_csv(clean_merged_books, 'data_clean/clean_merged_books.csv')
        load_data_to_csv(clean_books_data, 'data_clean/clean_books_data.csv')
        load_data_to_csv(clean_books_reviews, 'data_clean/clean_books_reviews.csv')

        # Simpan ke PostgreSQL
        load_data_to_postgres(clean_merged_books, 'clean_merged_books')
        load_data_to_postgres(clean_books_data, 'clean_books_data')
        load_data_to_postgres(clean_books_reviews, 'clean_books_reviews')

        return "Data loading completed successfully"
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data_wrapper,
    provide_context=True,
    dag=dag,
)

# Mengatur urutan task
extract_task >> transform_task >> load_task

if __name__ == "__main__":
    dag.cli()
