import pandas as pd
from datetime import date 
import plotly.express as px  
import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = dash.Dash(__name__)

cred = credentials.Certificate('/Users/Louis/Desktop/VIP/AIH_HIT-main/hit-with-database-794dbb2c512f.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

app = dash.Dash(external_stylesheets=[dbc.themes.COSMO])
# App layout
app.layout = html.Div([

    html.H1(id='patient_name',children=[], style={'text-align': 'left','margin-left': '2%'}),
    dbc.Button("back",id='back_D',size='sm',n_clicks=0,style={'margin-left': '2%',"background":'#ffffff','color':'black'}),
    html.Hr(style={'width':'90%','color':'black'}),
    html.Div([
    # dcc.DatePickerRange(
    #     id='my-date-picker-range',
    #     min_date_allowed=date(1995, 8, 5),
    #     max_date_allowed=date(2019, 9, 19),
    #     initial_visible_month=date(2017, 8, 5),
    #     end_date=date(2017, 8, 25)
    # ),
    html.H4(id='patient_age',children=[], style={'text-align': 'left','margin-left': '2%'}),
    ],style={'display': 'inline-block', 'vertical-align': 'top','margin-left': '2%'}),
    html.Div(children=[
    html.Embed(id='question',src="https://padnim14.github.io/survey-app/" , width="700", height="400", style={'border':'1px silver solid'}) ], 
    style={'display': 'inline-block', 'margin-left': '51vw', 'margin-top': '-2%'}),
    html.Hr(),
    html.Div(children=[
        dcc.Graph(id='plot_scatter',style={'display': 'inline-block'}),
        dcc.Graph(id='plot_bar',style={'display': 'inline-block'}) ],
        style={ 'vertical-align': 'top', 'margin-right': '0vw', 'margin-bottom': '3vh'}),
    dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds
        n_intervals=0),
    dcc.Location( id='link_D',href='',refresh=False)
]) 

@app.callback(
    Output('plot_scatter', 'figure'),
    Output('plot_bar','figure'),
    Input('interval-component', 'n_intervals'))
def plotgraphs(n):

    dfscat = pd.read_csv('ID 1003_heartrate_1min_20171001_20171007.csv')
    fig_scat = px.scatter(dfscat, x="Time", y="Value",title='Heart Rate')

    dfsbar = pd.read_csv('ID 1003_hourlyCalories_20171001_20171007.csv')
    fig_bar = px.bar(dfsbar, x="ActivityHour", y="Calories",title='Calories')

    return fig_scat,fig_bar

@app.callback(
    Output('patient_name', 'children'),
    Output('patient_age', 'children'),
    Input('interval-component', 'n_intervals'))
def patientinfo(n):

    query = db.collection(u'nurses').document(u'B12v6a5o3dGXGId8g02j').collection('patients').document(u'00ovyLEhdfps05n58MtA')
    patientdata= query.get()

    return (str(patientdata.to_dict().get('name')),
           "Age:" + str(patientdata.to_dict().get('age')) )

@app.callback(
    Output('link_D','href'),Output('link_D','refresh'),
    [Input('back_D', 'n_clicks')])
def gobacktoPatient(n_clicks):
    if n_clicks!=0:
        return ('/patients', True)
    else:
        return ('',False)



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)