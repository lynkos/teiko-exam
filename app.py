from dash import Dash, html, dcc
from load_data import DATABASE
from data_analysis import SUMMARY_TABLE_NAME
from sqlite3 import connect
import pandas
import dash_ag_grid as dag
import plotly.express as px
import scipy.stats as stats

# pip install "dash[cloud]"

connection = connect(DATABASE)

# Join summary table with sample table to get subject, then join with subject table to get response
data_frame = pandas.read_sql_query(
    f"""SELECT s.sample, s.total_count, s.population, s.count, s.percentage, t.subject, subj.response
        FROM {SUMMARY_TABLE_NAME} s
        JOIN samples t ON s.sample = t.sample
        JOIN subjects subj ON t.subject = subj.subject
    """, connection
)
connection.close()

app = Dash(__name__)

#server = app.server

# SUMMARY TABLE
app.layout = [
    html.Div(children = "Summary Table with Response"),
    dag.AgGrid(
        rowData = data_frame.to_dict("records"),
        columnDefs = [ { "field": i } for i in data_frame.columns ]
    ),
    dcc.Graph(figure = px.box(data_frame, x = "population", y = "percentage", color = "response", title = "Responders vs. Non-Responders Comparison"))
]

# BOXPLOT
populations = data_frame['population'].unique()
results = []

for pop in populations:
    df_pop = data_frame[data_frame['population'] == pop]
    yes = df_pop[df_pop['response'] == 'yes']['percentage']
    no = df_pop[df_pop['response'] == 'no']['percentage']
    if len(yes) > 1 and len(no) > 1:
        stat, pval = stats.ttest_ind(yes, no, equal_var=False)
        results.append({'population': pop, 'p-value': pval, 'mean_yes': yes.mean(), 'mean_no': no.mean()})
    else:
        results.append({'population': pop, 'p-value': None, 'mean_yes': yes.mean() if len(yes) > 0 else None, 'mean_no': no.mean() if len(no) > 0 else None})

# Print significant populations (p < 0.05)
sig = [r for r in results if r['p-value'] is not None and r['p-value'] < 0.05]
print('Populations with significant difference (p < 0.05):')
for r in sig:
    print(f"{r['population']}: p-value={r['p-value']:.4f}, mean_yes={r['mean_yes']:.2f}, mean_no={r['mean_no']:.2f}")

if __name__ == "__main__":
    app.run(debug = True)