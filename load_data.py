from sqlite3 import Connection, Cursor, connect
from csv import DictReader

# CONSTANTS
DATABASE: str = "subjects.db"
CSV: str = "cell-count.csv"

def validate_db(cursor: Cursor, table: str, column: str, value: str) -> bool:
    """
    Check if a value already exists in a given table

    Args:
        cursor (Cursor): Database cursor
        table (str): Table name
        column (str): Column name
        value (str): Value to check

    Returns:
        bool: True if value exists, else False
    """
    cursor.execute(f"SELECT 1 FROM {table} WHERE {column} = ?", (value,))
    return cursor.fetchone() is not None

def load_csv(connection: Connection, csv: str = CSV) -> None:
    """
    Load data from a CSV file into the database
    
    Args:
        connection (Connection): Database connection
        csv (str, optional): Path to the CSV file; defaults to CSV
    """
    cursor = connection.cursor()

    # Open given CSV file and read its contents
    with open(csv, mode = "r", newline = "", encoding = "utf-8") as file:
        csv_reader = DictReader(file, delimiter = ",")

        # Loop over each row in CSV file
        for row in csv_reader:
            # Extract value of 'subject' column in current row
            subject = row["subject"]

            # Check if current row's subject data already exists in 'subjects' table to avoid duplicates
            if not validate_db(cursor, "subjects", "subject", subject):
                # Insert current row's subject data into 'subjects' table
                cursor.execute("""
                    INSERT INTO subjects
                    (subject, project, condition, age, sex, treatment, response)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                        subject,
                        row["project"],
                        row["condition"],
                        int(row["age"]),
                        row["sex"],
                        row["treatment"],
                        row["response"] if row["response"] else None
                    )
                )
                print(f"Recorded '{subject}' in 'subjects' table in database")

            # Extract value of 'sample' column in current row
            sample = row["sample"]

            # Check if current row's sample data already exists in 'samples' table to avoid duplicates
            if not validate_db(cursor, "samples", "sample", sample):
                # Insert current row's sample data into 'samples' table
                cursor.execute("""
                    INSERT INTO samples
                    (sample, subject, sample_type, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                        sample,
                        subject,
                        row["sample_type"],
                        int(row["time_from_treatment_start"]) if row["time_from_treatment_start"] else None,
                        int(row["b_cell"]),
                        int(row["cd8_t_cell"]),
                        int(row["cd4_t_cell"]),
                        int(row["nk_cell"]),
                        int(row["monocyte"])
                    )
                )
                print(f"Recorded '{sample}' in 'samples' table in database")

    connection.commit()

def create_database(connection: Connection) -> None:
    """
    Create SQLite database
    
    Args:
        connection (Connection): Database connection
    """
    cursor = connection.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create 'subjects' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject TEXT PRIMARY KEY,
            project TEXT,
            condition TEXT,
            age INTEGER,
            sex TEXT CHECK(sex IN ('M', 'F')),
            treatment TEXT,
            response TEXT CHECK(response IN ('yes', 'no', ''))
        )
    """)
    print("Added 'subjects' table to database")

    # Create 'samples' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS samples (
            sample TEXT PRIMARY KEY,
            subject TEXT NOT NULL,
            sample_type TEXT,
            time_from_treatment_start INTEGER,
            b_cell INTEGER,
            cd8_t_cell INTEGER,
            cd4_t_cell INTEGER,
            nk_cell INTEGER,
            monocyte INTEGER,
            FOREIGN KEY (subject) REFERENCES subjects (subject)
        )
    """)
    print("Added 'samples' table to database")

    # Indexing for faster queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_samples_subject ON samples(subject)")

    connection.commit()

def main(database: str = DATABASE, csv: str = CSV) -> None:
    """
    Main function for Part 1: Data Management
        1. Create SQLite database
        2. Load data from CSV file into database

    Args:
        database (str, optional): Name of the SQLite database file; defaults to DATABASE
        csv (str, optional): Path to the CSV file; defaults to CSV
    """
    try:
        with connect(database) as connection:
            # 1. Create SQLite database
            print(f"Creating database '{database}'")
            create_database(connection)

            # 2. Load data from CSV file into database
            load_csv(connection, csv)
            print(f"Loaded data from '{csv}' into '{database}'")
            
    except Exception as e:
        print(f"An error occurred in main: {e}")

    finally:
        connection.close()

if __name__ == "__main__":
    main()