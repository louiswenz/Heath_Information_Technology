import dash
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from re import search
from firebase_admin import credentials
from firebase_admin import firestore

from app import app
from layout import layoutnurse_admin, layoutnurse_nurse,layoutpatient,patientDashboard,layoutAppointment
import callback


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa"
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-right": "0rem",
    "padding": "3rem 0rem",
    "background-color": "#eef2f6",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "Health Information Technology", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Dashboard", href="/", active="exact"),
                dbc.NavLink("Database", href="https://cloud.google.com/products/databases", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div([
    dcc.Location(id='url',refresh=False),
    html.Div(id='page-content',children=[])
])

@app.callback(Output('page-content', 'children'),Output('page-content', 'style'),Output('url','href'),
              Input('url', 'pathname'))
def display_page(pathname): 
    if '/patients' in pathname:
         return ([sidebar,layoutpatient],CONTENT_STYLE,'')
    if  '/nurses-admin' in pathname and callback.token==1:
        return ([sidebar,layoutnurse_admin],CONTENT_STYLE,'')
    if '/nurses-admin' in pathname and callback.token==0:
         return ([sidebar,layoutnurse_nurse],CONTENT_STYLE,'/nurses')
    if  '/nurses' in pathname:
         return ([sidebar,layoutnurse_nurse],CONTENT_STYLE,'')
    if  '/dashboard' in pathname:
         return (patientDashboard,{'':''},'')
    if '/appointment' in pathname:
        return (layoutAppointment,{'':''},'')
    else:
        return ([sidebar,layoutnurse_nurse],CONTENT_STYLE,'')           

if __name__ == '__main__':
    app.run_server(debug=False)

    