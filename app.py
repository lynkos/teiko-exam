from dash import Dash, html, dcc
from load_data import DATABASE
from data_analysis import SUMMARY_TABLE_NAME
from sqlite3 import connect
import pandas
import dash_ag_grid as dag
import plotly.express as px

# pip install "dash[cloud]"

connection = connect(DATABASE)

# Join summary table with sample table to get subject, then join with subject table to get response
data_frame = pandas.read_sql_query(
    f"""SELECT s.sample, s.total_count, s.population, s.count, s.percentage, t.subject, subj.response
    FROM {SUMMARY_TABLE_NAME} s
    JOIN samples t ON s.sample = t.sample
    JOIN subjects subj ON t.subject = subj.subject""",
    connection
)
connection.close()

app = Dash(__name__)

#server = app.server

app.layout = [
    html.Div(children = "Summary Table with Response"),
    dag.AgGrid(
        rowData = data_frame.to_dict("records"),
        columnDefs = [ { "field": i } for i in data_frame.columns ]
    ),
    dcc.Graph(figure = px.box(data_frame, x = "population", y = "percentage", color = "response"))
]

if __name__ == "__main__":
    app.run(debug = True)