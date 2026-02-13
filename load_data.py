import sqlite3
import csv

# CONSTANTS
DATABASE_NAME: str = "subjects.db"
CSV_FILE: str = "cell-count.csv"

def get_unique_vals(connection: sqlite3.Connection, table: str, column: str):
    cursor = connection.cursor()
    cursor.execute(f"SELECT DISTINCT {column} FROM {table}")
    return [row[0] for row in cursor.fetchall()]

def exists_in_db(connection: sqlite3.Connection, table: str, column: str, value: str) -> bool:
    cursor = connection.cursor()
    cursor.execute(f"SELECT 1 FROM {table} WHERE {column} = ?", (value,))
    return cursor.fetchone() is not None

def load_csv(connection: sqlite3.Connection, csv_file: str = CSV_FILE):
    cursor = connection.cursor()

    unique_subjects = set()
    
    num_rows = 0
    
    with open(csv_file, mode = "r", newline = "", encoding = "utf-8") as file:
        reader = csv.DictReader(file, delimiter = ",")

        for row in reader:
            subject = row["subject"]
            sample = row["sample"]
            
            # INSERT SUBJECT
            if subject not in unique_subjects:
                print(f"Inserting subject {subject} with sample {sample}")
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
                unique_subjects.add(subject)
                print(f"Subject {subject} inserted successfully")

            # INSERT SAMPLE
            print(f"Inserting sample {sample} for subject {subject}")
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

            num_rows += 1

    connection.commit()

    print(f"{num_rows} records successfully loaded")

def create_database(connection: sqlite3.Connection):
        cursor = connection.cursor()

        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")

        # SUBJECTS
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
        print("Created table: subjects")

        # SAMPLES
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
        print("Created table: samples")

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_samples_subject ON samples(subject)")

        connection.commit()

def main(database_name: str = DATABASE_NAME, csv_file: str = CSV_FILE):
    try:
        with sqlite3.connect(database_name) as connection:
            print(f"Creating database {database_name}")
            create_database(connection)

            print(f"Loading data from {csv_file} into database {database_name}")
            load_csv(connection, csv_file)

            print(get_unique_vals(connection, "samples", "sample_type"))

        print(f"Database {database_name} successfully created")

    except Exception as e:
        print(f"An error occurred in main: {e}")

    finally:
        connection.close()

if __name__ == "__main__":
    main()