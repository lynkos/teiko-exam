import sqlite3

# CONSTANTS
DATABASE_NAME: str = "patients.db"
CSV_FILE: str = "cell-count.csv"

def create_database(csv_file: str = CSV_FILE):
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            cursor = connection.cursor()

            # Execute SQL commands
            cursor.execute("")
            
    except Exception as e:
        print(f"An error occurred while creating {DATABASE_NAME}: {e}")

if __name__ == "__main__":
    create_database(CSV_FILE)