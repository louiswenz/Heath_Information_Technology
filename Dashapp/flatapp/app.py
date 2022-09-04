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


app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.COSMO])
server = app.server