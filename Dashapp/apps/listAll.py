import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
import dash_html_components as html
from re import search
import webbrowser
import time
#----------------------------------------------nurselist_layout----------------------------------------#
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("nurselist.csv"))

app = dash.Dash(external_stylesheets=[dbc.themes.COSMO], suppress_callback_exceptions=True)

layoutnurse = dbc.Container([
    html.H1(children='Nurses List'),
    dt.DataTable(
        id='tbl1', data=df.to_dict('records'),
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
    dbc.Modal(
            [
                dbc.ModalBody([
                    dcc.Interval(id="progress-interval", n_intervals=0, interval=1*1000), #1ms
                    dbc.Progress(id="progress")]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close1", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal1",
            is_open=False,
        ),
    #dbc.Alert(id='tbl_out'),
])

#callback for progress modal
@app.callback(
    Output('modal1', 'is_open'),
    Input('tbl1', 'active_cell'), Input("close1", "n_clicks")
    ,[State("modal1", "is_open")])
def toggle_modal(active_cell, n2, is_open):
    if  n2:
        return not is_open
    elif search("progress",str(active_cell))==1:
        return is_open

#callback for progress calculation, change later
@app.callback(
    [Output("progress", "value"), Output("progress", "children")],
    [Input("progress-interval", "n_intervals")],
)
def update_progress(n):
    # check progress of some background process, in this example we'll just
    # use n_intervals constrained to be in 0-100
    progress = min(n % 110, 100)
    # only add text after 5% progress to ensure text isn't squashed too much
    return progress, f"{progress} %" if progress >= 5 else ""
#----------------------------------------------nurselist_layout----------------------------------------#

#----------------------------------------------patientlist_layout----------------------------------------#
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df2 = pd.read_csv(DATA_PATH.joinpath("patientlist.csv"))

#app = dash.Dash(external_stylesheets=[dbc.themes.COSMO])

layoutpatient = dbc.Container([
    html.H1(children='Paitents List'), dbc.Button("Back",id='back',style={'display': 'inline-block'}),
    html.Br(),
    dbc.Button('Add New Patient', id='button2',style={'display': 'inline-block','border':'none','background-color':'white','color':'black','margin-left': '982px','height': '33px'}),
    dt.DataTable(
        id='tbl2', data=df2.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df2.columns],
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
    dbc.Modal(
            [
                dbc.ModalBody(html.Embed(src='https://ktong2023.github.io/test/',height="500",width="470",style={'matgin-top':'400vw'})),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close2", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal2",
            is_open=False,
        )
])

#callback for add patients
@app.callback(
    Output("modal2", "is_open"),
    [Input("button2", "n_clicks"), Input("close2", "n_clicks")],
    [State("modal2", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



#----------------------------------------------patientlist_layout----------------------------------------#
app.layout = html.Div([
    #dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[layoutnurse])
])
#decide which page to open
@app.callback(Output('page-content', 'children'), 
Input('tbl1', 'active_cell'))#, Input("Back", "n_clicks"))
def update_page(active_cell):
    if search("Patients",str(active_cell)):
        return layoutpatient
    # elif n1:
    #      return layoutnurse
    else:
        return layoutnurse


if __name__ == '__main__':
    app.run_server(debug=True)