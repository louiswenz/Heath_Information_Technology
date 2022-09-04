import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H2('Thank Mbkupfer for this modal'),
    dbc.Button('Add New Patient', id='button'),

    html.Div(children=[],
        id='modal',
        className='modal',
        style={"display": "block"},
    )
])
@app.callback(
    Output('modal', 'children'),
    Input('button', 'n_clicks'))
def defmod(n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'button' in changed_id:
        return html.Div([  # content div
            html.Div([
                html.Embed(src='http://www.google.com'),

            ]),

            html.Hr(),
            dbc.Button('Close', href='http://127.0.0.1:8050/',id='modal-close-button')
        ],
            style={'textAlign': 'center', },
            className='modal-content',
        )





# @app.callback(Output('modal', 'style'),
#               [Input('modal-close-button', 'n_clicks')])
# def close_modal(n):
#     if (n is not None) and (n > 0):
#         return {"display": "none"}




if __name__ == '__main__':
    app.run_server(debug=True)