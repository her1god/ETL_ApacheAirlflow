import os
import pandas as pd
import sqlite3

def find_file(filename, search_path="."):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def extract_book_details():
    file_path = find_file("Book_Details.csv")
    if file_path:
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError("Book_Details.csv not found")

def extract_book_reviews():
    file_path = find_file("book_reviews.db")
    if file_path:
        conn = sqlite3.connect(file_path)
        return pd.read_sql_query("SELECT * FROM book_reviews", conn)
    else:
        raise FileNotFoundError("book_reviews.db not found")

def extract_books():
    file_path = find_file("books.db")
    if file_path:
        conn = sqlite3.connect(file_path)
        return pd.read_sql_query("SELECT * FROM books", conn)
    else:
        raise FileNotFoundError("books.db not found")