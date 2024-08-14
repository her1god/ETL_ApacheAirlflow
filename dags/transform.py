import pandas as pd
import re

def transform_book_details(book_details_df):
    def convert_date(date_str):
        try:
            return pd.to_datetime(date_str, format='%B %d, %Y')
        except ValueError:
            return pd.NaT

    book_details_df['publication_info'] = book_details_df['publication_info'].str.replace(r'\[.*published\s+', '', regex=True).str.strip("']")
    book_details_df['publication_info'] = book_details_df['publication_info'].apply(convert_date)
    book_details_df = book_details_df.dropna(subset=['publication_info']).copy()

    book_details_df['format'] = book_details_df['format'].str.extract(r'(\s*\w+\s*[A-Za-z0-9]+\s*)\']$')
    book_details_df['format'] = book_details_df['format'].str.strip("[]'")
    book_details_df['num_pages'] = book_details_df['num_pages'].str.strip("[]'")

    book_details_df['num_pages'] = book_details_df['num_pages'].replace(['None', ''], 0).astype(int)
    book_details_df['book_details'] = book_details_df['book_details'].fillna("Tidak Ada Ringkasan Tersedia")

    return book_details_df

def transform_book_reviews(book_reviews_df):
    book_reviews_df['book_id'] = book_reviews_df['book_id'].astype(int)
    book_reviews_df['likes_on_review'] = book_reviews_df['likes_on_review'].str.replace("likes", "")
    book_reviews_df['reviewer_total_reviews'] = book_reviews_df['reviewer_total_reviews'].str.replace("reviews", "")
    book_reviews_df['reviewer_followers'] = book_reviews_df['reviewer_followers'].str.replace(r'\bfollowers?\b', '', regex=True).str.strip()

    book_reviews_df = book_reviews_df[book_reviews_df['reviewer_followers'] != 'Author'].copy()

    def remove_k_and_convert_to_int(value):
        if pd.isnull(value):
            return None
        numeric_value = re.sub(r'[^\d.]', '', value)
        return float(numeric_value)

    columns_to_process = ['likes_on_review', 'reviewer_total_reviews', 'reviewer_followers']
    for col in columns_to_process:
        book_reviews_df[col] = book_reviews_df[col].apply(remove_k_and_convert_to_int)

    book_reviews_df[columns_to_process] = book_reviews_df[columns_to_process].fillna(0).astype(int)
    book_reviews_df['review_date'] = pd.to_datetime(book_reviews_df['review_date'], format='%B %d, %Y')
    book_reviews_df['review_rating'] = book_reviews_df['review_rating'].fillna('Rating 0 out of 5')
    book_reviews_df['review_rating'] = book_reviews_df['review_rating'].str.replace(r'Rating (\d) out of 5', r'\1', regex=True).astype(int)

    return book_reviews_df

def transform_books(books_df):
    return books_df.rename(columns={'id': 'book_id'})
