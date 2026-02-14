from dash import Dash, html
from load_data import DATABASE
from data_analysis import SUMMARY_TABLE_NAME
from sqlite3 import connect
import pandas
import dash_ag_grid as dag

connection = connect(DATABASE)

data_frame = pandas.read_sql_query(f"SELECT sample, total_count, population, count, percentage FROM {SUMMARY_TABLE_NAME}", connection)

app = Dash()

#server = app.server

app.layout = [
    html.Div(children = 'My First App with Data'),
    dag.AgGrid(
        rowData = data_frame.to_dict("records"),
        columnDefs = [{"field": i} for i in data_frame.columns]
    )
]

if __name__ == "__main__":
    app.run(debug = True)