import dash
from dash.dependencies import Input, Output, State
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

app = dash.Dash(suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.COSMO])

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
    dbc.Modal(
            [
                dbc.ModalBody([
                    dcc.Interval(id="progress-interval", n_intervals=0, interval=1*1000), #1ms
                    dbc.Progress(id="progress", style={'height':'20px'})]),
                    html.Br(),
                    html.H5("Add task", style={'marginLeft':'15px', 'font-weight': '400'}),
                    dcc.Input(
                        id='tasknameinput',
                        type='text',
                        placeholder='enter task name here', style={'marginLeft':'15px','marginRight':'150px'}),
                    html.Br(),
                    dbc.Button("Submit",id="submit_task", n_clicks=0,
                    style={'background-color':'white','color':'black','marginLeft':'15px','marginRight':'400px'},size='sm'),
                html.Hr(),#
                html.Div(id='task_checklist', children=[] ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    dbc.Alert(id='tbl_out'),
    dcc.Location( id='link',href='',refresh=False)
])

@app.callback(Output('tbl_out', 'children'), Output('link', 'href'),
              Input('tbl', 'active_cell'))
def update_graphs(active_cell):
    if search("Patients",str(active_cell)):
        #webbrowser.open('http://127.0.0.1:8050/apps/patientlist')
        #dcc.Link('',href='/p2')
        return (str(active_cell), '/p2')
    elif search("Location",str(active_cell)):
        webbrowser.open('http://www.yahoo.com')
        return ("opened Location page", 'p3')
    else:
        return ("",'')

@app.callback(
    Output('modal', 'is_open'), Output('close', 'n_clicks'),
    Input('tbl', 'active_cell'), Input("close", "n_clicks")
    ,[State("modal", "is_open")])
def toggle_modal(active_cell, n2, is_open):
    if search("Progress",str(active_cell))!=None or n2!=0:
        return (not is_open, 0)
    else:
        return ('',0)

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


@app.callback(
    Output('task_checklist','children'),Output('submit_task','n_clicks'),
    Input('submit_task','n_clicks'),Input('tasknameinput','value'),
    [State('task_checklist','children')])
def more_output(n_clicks,value,prevContent):
    if n_clicks==0:
        raise dash.exceptions.PreventUpdate
    elif n_clicks>0:
        if value is not None:
            return ( prevContent + [ html.Div( dbc.Checklist(options=[{'label': " "+str(value),'value':str(value)}], persisted_props=['value'], persistence=True, persistence_type='session',
                 style={'marginLeft':'15px'} )) ] , 0)
        else:return ( prevContent , 0)

if __name__ == "__main__":
    app.run_server(debug=True)