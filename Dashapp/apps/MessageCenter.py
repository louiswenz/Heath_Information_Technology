import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from twilio.rest import Client

account_sid = 'AC18f4cc68aa19dffc73cf35a14b240990'
auth_token = '6bf7a8633d5c69f11314decadc9f3310'
client = Client(account_sid, auth_token)

shortcut1='Hi, you have an upcoming appointment'
shortcut2='Please complete the survey: https://padnim14.github.io/survey-app/'
shortcut3='Your medicine is ready to pick up'

app = dash.Dash(__name__)
app.layout = html.Div([
    html.Br(),
    dcc.Dropdown(
        id='shortcuts',
        options=[
            {'label': shortcut1, 'value': shortcut1},
            {'label': shortcut2, 'value': shortcut2},
            {'label': shortcut3, 'value': shortcut3}
        ],
        placeholder='Select one short cut to send',
        style={'width':'60%','padding':'5px'}
    ),
    html.Br(),html.Br(),
    dcc.Input(id='custom_txt',type="text", placeholder="Or send a custom message",debounce=True, persistence=False,style={'margin-left':'5px','width':'60%','padding':'10px'}),
    html.Br(),html.Br(),html.Hr(),
    dbc.Button("Send",id="send_message",n_clicks=0,style={'display': 'block','margin-left':'5px',}),
    dcc.ConfirmDialog(
        id='confirmation_sms',
        message='Text message sent successfully',
    ),
])

@app.callback(
    Output('confirmation_sms', 'displayed'),Output('shortcuts', 'value'),Output('custom_txt', 'value'),
    Output('send_message', 'n_clicks'),
    Input('shortcuts', 'value'),Input('custom_txt','value'),Input('send_message','n_clicks'))
def send_text(shortcut, custom_txt,n_clicks):
    if (n_clicks>0) & (custom_txt is not None):
            message = client.messages \
                                .create(
                                    body=custom_txt,
                                    from_='+12078257270',
                                    to='+17172030525'
                                )
            return (True,None,None,0)
    if (n_clicks>0) & (shortcut is not None):
            message = client.messages \
                                .create(
                                    body=shortcut,
                                    from_='+12078257270',
                                    to='+17172030525'
                                )
            return (True,None,None,0)
    else:
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)