from dash import Dash, html, dcc
import dash_ag_grid as dag
import plotly.express as px
from stats_analysis import DATA_FRAME, COMPARISON, DATA_FRAME_SUMMARY, DATA_FRAME2
from subset_analysis import DATA_FRAME_PROJECTS, DATA_FRAME_RESPONDERS, DATA_FRAME_SEXES, DATA_FRAME_FILTER

# pip install "dash[cloud]"

# CONSTANTS
HEADER_SIZE = 25
FONT_SIZE = 18

app = Dash(__name__, title = "Teiko Exam - Data Analysis")

app.layout = [
    html.H1(children = "Part 2: Initial Analysis - Data Overview",
            style = { 'textAlign': 'center', 'fontSize': HEADER_SIZE }),
    html.H2(children = "Summary Table",
            style = { 'textAlign': 'center', 'fontSize': FONT_SIZE }),
    dag.AgGrid(
        rowData = DATA_FRAME_SUMMARY.to_dict("records"),
        columnDefs = [ { "field": i } for i in DATA_FRAME_SUMMARY.columns ]
    ),

    html.H1(children = "Part 3: Statistical Analysis",
            style = { 'textAlign': 'center', 'fontSize': HEADER_SIZE }),
    
    # BOXPLOT
    dcc.Graph(figure = px.box(DATA_FRAME, x = "population", y = "percentage", color = "response", title = "Relative frequencies of responders vs. non-responders for each cell population")),

    html.H2(children = "Differences in relative frequencies between responders vs. non-responders for each cell population",
            style = { 'textAlign': 'center', 'fontSize': FONT_SIZE }),
    dag.AgGrid(
        rowData = COMPARISON.to_dict("records"),
        dashGridOptions = { "domLayout": "autoHeight" },
        columnSize = "responsiveSizeToFit",
        columnDefs = [ { "field": i } for i in COMPARISON.columns ]
    ),

    html.H1(children = "Part 4: Data Subset Analysis",
            style = { 'textAlign': 'center', 'fontSize': HEADER_SIZE }),

    html.H2(children = "1. All melanoma PBMC samples at baseline from patients treated with miraclib",
            style = { 'textAlign': 'center', 'fontSize': FONT_SIZE }),
    dag.AgGrid(
        rowData = DATA_FRAME_FILTER.to_dict("records"),
        columnSize = "responsiveSizeToFit",
        columnDefs = [ { "field": i } for i in DATA_FRAME_FILTER.columns ]
    ),

    html.H2(children = "2. How many samples from each project",
            style = { 'textAlign': 'center', 'fontSize': FONT_SIZE }),
    dag.AgGrid(
        rowData = DATA_FRAME_PROJECTS.to_dict("records"),
        dashGridOptions = { "domLayout": "autoHeight" },
        columnSize = "responsiveSizeToFit",
        columnDefs = [ { "field": i } for i in DATA_FRAME_PROJECTS.columns ]
    ),

    html.H2(children = "3. How many subjects were responders/non-responders",
            style = { 'textAlign': 'center', 'fontSize': FONT_SIZE }),
    dag.AgGrid(
        rowData = DATA_FRAME_RESPONDERS.to_dict("records"),
        dashGridOptions = { "domLayout": "autoHeight" },
        columnSize = "responsiveSizeToFit",
        columnDefs = [ { "field": i } for i in DATA_FRAME_RESPONDERS.columns ]
    ),

    html.H2(children = "4. How many subjects were males/females",
            style = { 'textAlign': 'center', 'fontSize': FONT_SIZE }),
    dag.AgGrid(
        rowData = DATA_FRAME_SEXES.to_dict("records"),
        dashGridOptions = { "domLayout": "autoHeight" },
        columnSize = "responsiveSizeToFit",
        columnDefs = [ { "field": i } for i in DATA_FRAME_SEXES.columns ]
    )
]

if __name__ == "__main__":
    app.run(debug = True)