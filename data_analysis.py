from sqlite3 import Connection, connect
from uuid import uuid4
from load_data import CELL_TYPES

SUMMARY_TABLE_NAME: str = "summary_table"
"""Name of summary table"""

DATABASE: str = "subjects.db"
"""SQLite database path"""

def populate_summary_table(connection: Connection, table: str = SUMMARY_TABLE_NAME) -> None:
    """
    Populate summary table with the following for each sample (i.e. row):
        - id: Unique ID for each row
        - sample: Sample ID (i.e. 'sample' column in .csv)
        - total_count: Sample's total cell count (i.e. sum of all cell population counts for that sample)
        - population: Immune cell population's name (e.g. b_cell, cd8_t_cell, etc.)
        - count: Cell count
        - percentage: Relative frquency of the cell population (in percentage)

    Args:
        connection (Connection): Database connection
        table (str, optional): Table name; defaults to SUMMARY_TABLE_NAME
    """
    cursor = connection.cursor()

    print("Fetching sample data")
    sample_data = cursor.execute(f"SELECT sample, {', '.join(CELL_TYPES)} FROM samples").fetchall()

    # Loop over each sample
    for sample in sample_data:
        # Get sample ID and cell population counts from current sample
        sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte = sample

        cell_columns = [ b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte ]

        # Calculate total cell count for current sample
        total_count = sum(cell_columns)
        print(f"Total count for sample '{sample_id}': {total_count}")

        # Loop over each cell population in sample
        for population, count in zip(CELL_TYPES, cell_columns):
            # Calculate relative frequency of current cell population in sample
            frequency = (count / total_count) * 100 if total_count > 0 else 0
            
            print(f"Processing '{population}' in sample '{sample_id}' with count {count} and frequency {frequency:.2f}%")

            # Insert a row into summary table with the following column values:
            # 1. Row's unique ID
            # 2. Sample ID
            # 3. Sample's total count
            # 4. Cell population name
            # 5. Cell count for population
            # 6. Relative frequency of cell population in sample
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
                    frequency
                )
            )
            print(f"Inserted sample '{sample_id}' into {table}")

    connection.commit()

    print(f"Finished populating {table} table in database")

def create_summary_table(connection: Connection, table: str = SUMMARY_TABLE_NAME):
    """
    Create summary table with these columns for each sample:
        - id: Unique ID for each row
        - sample: Sample ID (i.e. 'sample' column in .csv)
        - total_count: Sample's total cell count (i.e. sum of all cell population counts for that sample)
        - population: Immune cell population's name (e.g. b_cell, cd8_t_cell, etc.)
        - count: Cell count
        - percentage: Relative frquency of the cell population (in percentage)

    Args:
        connection (Connection): Database connection
        table (str, optional): Table name; defaults to SUMMARY_TABLE_NAME
    """
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
    print(f"Added '{table}' table to database")

    connection.commit()

def main(database: str = DATABASE, summary_table: str = SUMMARY_TABLE_NAME) -> None:
    """
    Main function for Part 2: Initial Analysis - Data Overview
        1. Create summary table in database
        2. Populate summary table in database

    Args:
        database (str, optional): Name of the SQLite database file; defaults to DATABASE
        summary_table (str, optional): Summary table name; defaults to SUMMARY_TABLE_NAME
    """
    try:
        with connect(database) as connection:
            print(f"Creating {summary_table} table in '{database}'")
            create_summary_table(connection, summary_table)

            print(f"Populated {summary_table} table in '{database}'")
            populate_summary_table(connection, summary_table)
                        
    except Exception as e:
        print(f"An error occurred in main: {e}")

    finally:
        connection.close()

if __name__ == "__main__":
    main()