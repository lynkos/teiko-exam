from dash import Dash, html, dcc
import dash_ag_grid as dag
import plotly.express as px
from stats_analysis import DATA_FRAME, COMPARISON, DATA_FRAME_summary, DATA_FRAME2
from subset_analysis import DATA_FRAME_PROJECTS, DATA_FRAME_RESPONDERS, DATA_FRAME_SEXES, DATA_FRAME_FILTER

# pip install "dash[cloud]"

app = Dash(__name__)

#server = app.server

app.layout = [
    # SUMMARY TABLE
    html.Div(children = "Summary Table"),
    dag.AgGrid(
        rowData = DATA_FRAME_summary.to_dict("records"),
        columnDefs = [ { "field": i } for i in DATA_FRAME_summary.columns ]
    ),
    
    # BOXPLOT
    html.Div(children = "Relative frequencies of responders vs. non-responders for each cell population"),
    dcc.Graph(figure = px.box(DATA_FRAME, x = "population", y = "percentage", color = "response", title = "Responders vs. Non-Responders Comparison")),

    html.Div(children = " Differences in relative frequencies between responders and non-responders for all cell populations"),
    dag.AgGrid(
        rowData = COMPARISON.to_dict("records"),
        columnDefs = [ { "field": i } for i in COMPARISON.columns ]
    ),
    
    html.Div(children = "All melanoma PBMC samples at baseline from patients treated with miraclib"),
    dag.AgGrid(
        rowData = DATA_FRAME_FILTER.to_dict("records"),
        columnDefs = [ { "field": i } for i in DATA_FRAME_FILTER.columns ]
    ),

    html.Div(children = "How many samples from each project"),
    dag.AgGrid(
        rowData = DATA_FRAME_PROJECTS.to_dict("records"),
        columnDefs = [ { "field": i } for i in DATA_FRAME_PROJECTS.columns ]
    ),

    html.Div(children = "How many subjects were responders"),
    dag.AgGrid(
        rowData = DATA_FRAME_RESPONDERS.to_dict("records"),
        columnDefs = [ { "field": i } for i in DATA_FRAME_RESPONDERS.columns ]
    ),

    html.Div(children = "How many subjects were males/females"),
    dag.AgGrid(
        rowData = DATA_FRAME_SEXES.to_dict("records"),
        columnDefs = [ { "field": i } for i in DATA_FRAME_SEXES.columns ]
    ),
]

if __name__ == "__main__":
    app.run(debug = True)