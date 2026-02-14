from dash import Dash, html, dcc
import dash_ag_grid as dag
import plotly.express as px
from stats_analysis import DATA_FRAME, DATA_FRAME2

# pip install "dash[cloud]"

app = Dash(__name__)

#server = app.server

app.layout = [
    # SUMMARY TABLE
    html.Div(children = "Summary Table with Response"),
    dag.AgGrid(
        rowData = DATA_FRAME.to_dict("records"),
        columnDefs = [ { "field": i } for i in DATA_FRAME.columns ]
    ),
    # BOXPLOT
    dcc.Graph(figure = px.box(DATA_FRAME, x = "population", y = "percentage", color = "response", title = "Responders vs. Non-Responders Comparison")),
    dag.AgGrid(
        rowData = DATA_FRAME2.to_dict("records"),
        columnDefs = [ { "field": i } for i in DATA_FRAME2.columns ]
    ),
]

if __name__ == "__main__":
    app.run(debug = True)