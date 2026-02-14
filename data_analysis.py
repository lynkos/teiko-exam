from sqlite3 import Connection, connect
from uuid import uuid4
import pandas

# CONSTANTS
SUMMARY_TABLE_NAME: str = "summary_table"
DATABASE: str = "subjects.db"

def print_summary_table(connection: Connection, table: str = SUMMARY_TABLE_NAME) -> None:
    data_frame = pandas.read_sql_query(f"SELECT sample, total_count, population, count, percentage FROM {table}", connection)
    print(data_frame.to_string(index = False))

def populate_summary_table(connection: Connection, table: str = SUMMARY_TABLE_NAME) -> None:
    cursor = connection.cursor()

    sample_data = cursor.execute("SELECT sample, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte FROM samples").fetchall()

    for sample in sample_data:
        sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte = sample

        cell_columns = [ b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte ]

        total_count = sum(cell_columns)

        for population, count in zip(
            [ "b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte" ],
            cell_columns
        ):
            cursor.execute(f"""
                INSERT INTO {table}
                (id, sample, total_count, population, count, percentage)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                    str(uuid4()),
                    sample_id,
                    total_count,
                    population,
                    count,
                    (count / total_count) * 100 if total_count > 0 else 0
                )
            )

    connection.commit()

def create_summary_table(connection: Connection, table: str = SUMMARY_TABLE_NAME):
    cursor = connection.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create summary table
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
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

def main(database: str = DATABASE, table: str = SUMMARY_TABLE_NAME) -> None:
    try:
        with connect(database) as connection:
            print(f"Creating new table in '{database}'")
            create_summary_table(connection, table)
            
            populate_summary_table(connection, table)
            
            print_summary_table(connection, table)
            
    except Exception as e:
        print(f"An error occurred in main: {e}")

    finally:
        connection.close()

if __name__ == "__main__":
    main()