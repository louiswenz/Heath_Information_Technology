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

df = pd.read_csv(DATA_PATH.joinpath("patientlist.csv"))

app = dash.Dash(external_stylesheets=[dbc.themes.COSMO])

app.layout = dbc.Container([
    html.H1(children='Paitents List'),
    html.Br(),
    dbc.Button('Add New Patient', id='button',style={'display': 'inline-block','border':'none','background-color':'white','color':'black','margin-left': '982px','height': '33px'}),
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
    dbc.Alert(id='tbl_out'),
    dbc.Modal(
            [
                dbc.ModalBody(html.Embed(src='https://ktong2023.github.io/test/',height="500",width="470",style={'matgin-top':'400vw'})),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        )
])

@app.callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
def update_graphs(active_cell):
    if search("Patients",str(active_cell)):
        webbrowser.open('http://www.google.com')
        return "opened patient profile"
    elif search("Location",str(active_cell)):
        webbrowser.open('http://www.yahoo.com')
        return "opened Location page"
    else:
        return ""

# @app.callback(
#     Output('modal', 'children'),
#     Input('button', 'n_clicks'))
# def defmod(n_clicks):
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if 'button' in changed_id:
#         return html.Div([  # content div
#                 html.Embed(src='https://ktong2023.github.io/test/',height="500",style={'matgin-top':'400vw'}),

#             dbc.Button('Close', href='http://127.0.0.1:8050/',id='modal-close-button')
#         ],
#             style={'margin-left':'0vw','top':'5%','border':'1px silver solid'},
#             className='modal-content',
#         )
@app.callback(
    Output("modal", "is_open"),
    [Input("button", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open




if __name__ == "__main__":
    app.run_server(debug=True)