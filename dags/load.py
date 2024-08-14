import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

def load_data_to_csv(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        logging.info(f"Data successfully saved to CSV: {file_path}")
    except Exception as e:
        logging.error(f"Error saving data to CSV {file_path}: {e}")

def load_data_to_postgres(df, table_name):
    try:
        # Get database credentials from environment variables
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        host = os.getenv('POSTGRES_HOST')
        port = os.getenv('POSTGRES_PORT')
        db = os.getenv('POSTGRES_DB')

        logging.info(f"Postgres user: {user}, host: {host}, port: {port}, db: {db}")

        # Create a SQLAlchemy engine using environment variables
        engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')
        
        logging.info(f"Engine created successfully. Engine URL: {engine.url}")

        # Test the engine by connecting to the database
        with engine.connect() as connection:
            logging.info("Successfully connected to the database")

        # Save DataFrame to PostgreSQL using the engine
        df.to_sql(table_name, engine, index=False, if_exists='replace')
        
        logging.info(f"Data successfully saved to PostgreSQL table: {table_name}")
    except Exception as e:
        logging.error(f"Error occurred while saving data to PostgreSQL table {table_name}: {e}")
        logging.error(f"Exception details: {e}", exc_info=True)

