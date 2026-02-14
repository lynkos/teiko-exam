from sqlite3 import Connection, connect
from uuid import uuid4
import pandas

# CONSTANTS
DATABASE: str = "subjects.db"

def populate_table(connection: Connection) -> None:
    cursor = connection.cursor()

    sample_data = cursor.execute("SELECT sample, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte FROM samples").fetchall()

    for sample in sample_data:
        sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte = sample

        total_count = b_cell + cd8_t_cell + cd4_t_cell + nk_cell + monocyte

        for population, count in zip(
            ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"],
            [b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte] # sample[1:]
        ):
            unique_id = str(uuid4())
            percentage = (count / total_count) * 100 if total_count > 0 else 0
            cursor.execute("""
                INSERT INTO cell_frequency
                (id, sample, total_count, population, count, percentage)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                    unique_id,
                    sample_id,
                    total_count,
                    population,
                    count,
                    percentage
                )
            )

        print(f"Processed sample '{sample_id}' and inserted cell frequency data into 'cell_frequency' table")

    connection.commit()

def create_table(connection: Connection):
    cursor = connection.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create 'cell_frequency' table with composite primary key
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cell_frequency (
            id TEXT PRIMARY KEY,
            sample TEXT,
            total_count INTEGER,
            population TEXT,
            count INTEGER,
            percentage REAL,
            FOREIGN KEY (sample) REFERENCES samples (sample)
        )
    """)

    connection.commit()

def main(database: str = DATABASE) -> None:
    try:
        with connect(database) as connection:
            print(f"Creating new table in '{database}'")
            create_table(connection)
            populate_table(connection)
            print(f"Populated 'cell_frequency' table in '{database}'")
            
    except Exception as e:
        print(f"An error occurred in main: {e}")

    finally:
        connection.close()

if __name__ == "__main__":
    main()