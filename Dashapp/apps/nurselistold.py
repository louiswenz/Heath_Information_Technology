import dash
from dash.dependencies import Input, Output
import dash_table as dt
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from re import search
import webbrowser

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("nurselist.csv"))

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1(children='Nurses List'),
    dt.DataTable(
        id='tbl', data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    },
    style_as_list_view=True,
    filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
    ),
    dbc.Alert(id='tbl_out')
])

@app.callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
def update_graphs(active_cell):
    if search("Patients",str(active_cell)):
        webbrowser.open('http://www.google.com')
        return str(active_cell)
    elif search("Location",str(active_cell)):
        webbrowser.open('http://www.yahoo.com')
        return "opened Location page"
    else:
        return ""

if __name__ == "__main__":
    app.run_server(debug=True)