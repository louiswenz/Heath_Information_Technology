import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import dash_auth

import dash_core_components as dcc
import dash_html_components as html

token = 0

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[])
server=app.server

login_page = html.Div([
html.Div(
dcc.Input(id="user", type="text", placeholder="Enter Username",className="inputbox1",
style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'60px',
'font-size':'16px','border-width':'3px','border-color':'#a0a3a2'
}),
),
html.Div(
dcc.Input(id="passw", type="text", placeholder="Enter Password",className="inputbox2",
style={'margin-left':'35%','width':'450px','height':'45px','padding':'10px','margin-top':'10px',
'font-size':'16px','border-width':'3px','border-color':'#a0a3a2',
}),
),
html.Div(
html.Button('Verify', id='verify', n_clicks=0, style={'border-width':'3px','font-size':'14px'}),
style={'margin-left':'45%','padding-top':'30px'}),
dbc.Alert(id='output1')
])

logged = html.Div(
    [
        html.H2("ur r logged in")
    ]
)

not_logged = html.Div(
    [
        html.H2("ur r not logged in")
    ]
)

app.layout = html.Div([
    dcc.Location(id='url',refresh=False),
    dbc.Button("Get login",id='login',n_clicks=0),
    html.Div(id='page-content',children=[])
])

@app.callback(
    Output('output1', 'children'),Output('url', 'href'),
   [Input('verify', 'n_clicks')],
    state=[State('user', 'value'),
                State('passw', 'value')])
def update_output(n_clicks, uname, passw):
    global token
    li={'louis':'123'}
    if uname =='' or uname == None or passw =='' or passw == None:
        return ('','')
    if uname not in li:
        return ('Incorrect Username','/notlogged')
    if li[uname]==passw:
        token=1
        return ('Access Granted!','/logged')
    else:
        return ('Incorrect Password','/notlogged')

@app.callback(Output('page-content', 'children'),Output('login','n_clicks'),
              Input('url', 'pathname'),Input('login','n_clicks'))
def display_page(pathname,n_clicks):
    global token
    if n_clicks>0:
        return (login_page,0)
        
    if '/logged' in pathname and token==1:
         return (logged,0)
    if  '/notlogged' in pathname:
         return (not_logged,1)
    else:
        return ('404',0)


if __name__ == '__main__':
    app.run_server(debug=True)

    





