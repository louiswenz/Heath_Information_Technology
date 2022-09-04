import dash
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from re import search
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pickle
from datetime import date,datetime, timedelta

# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../datasets").resolve()

# df = pd.read_csv(DATA_PATH.joinpath("nurselist.csv"))

# Initialize database connection
cred = credentials.Certificate('/Users/Louis/Desktop/VIP/AIH_HIT-main/hit-with-database-794dbb2c512f.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

#------------below is login for admin login layout------------------#
login_page = html.Div([
    html.Br(),html.Br(),html.Br(),
    html.Div(
    dcc.Input(id="user", type="text", placeholder="Enter Username",className="inputbox1",
    style={'width':'100%','padding':'10px'}),
    ),
    html.Br(),html.Br(),
    html.Div(
    dcc.Input(id="passw", type="password", placeholder="Enter Password",className="inputbox2",
    style={'width':'100%','padding':'10px'}),
    ),
    html.Br(),html.Br(),
    html.Div(
    dbc.Button('Verify', id='verify', n_clicks=0, style={'width':'20%','margin-left':'40%'}),),
    html.Br(),html.Br(),html.Br(),
    dbc.Alert(id='output1')
])

#----------below is nurselayout_admin--------#

# volatile globals

nurse_array = []
nurse_id_array = []
curr_nurse_id = ''

patient_array = []
patient_id_array = []
curr_patient_id = ''

layoutnurse_admin= dbc.Container([
    html.H1(children='Nurses List'),
    dbc.Button("Sign out",id='signout_button',n_clicks=0,style={'margin-left':'93%','color':'#ed8413','background-color':'transparent','border':'none'}),
    dt.DataTable(
        id='tbln_admin',
        columns=[{"name": "Name", "id": "name"}, {"name": "Nurse ID", "id": "nurse_id"}, {"name": "Check in time", "id": "checkin_time"}, 
        {"name": "Status", "id": "status"},{"name": "New task", "id": "create_task"},{"name": "Progress", "id": "progress_link"},{"name": "Patients", "id": "patient_link"}],
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
                    dcc.Interval(id="create_task_interval_admin", n_intervals=0, interval=1*1000), #1ms
                    ]),
                    html.Br(),
                    html.H5("Add tasks", style={'marginLeft':'15px', 'font-weight': '400'}),
                    dcc.Input(
                        id='tasknameinput_admin',
                        type='text',
                        placeholder='enter task name here', style={'marginLeft':'15px','marginRight':'150px'}),
                    html.Br(),
                    dbc.Button("Submit",id="submit_task_admin", n_clicks=0,
                    style={'background-color':'white','color':'black','marginLeft':'15px','marginRight':'400px'},size='sm'),
            html.Hr(),
            html.Div(id='task_checklist_admin', children=[] ),
            dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_N_admin", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modaln_admin",
            is_open=False,
        ),
    dbc.Modal(
            [
            dbc.ModalBody([
                    dcc.Interval(id="view_progress_interval_admin", n_intervals=0, interval=1*1000), #1ms
                    html.H3("Tasks", style={'marginLeft':'15px', 'font-weight': '400'}),
                    ]),
                    html.Hr(),
                    html.Br(),
            html.Div(id='task_checklist_admin', children=[] ),
            dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_N_view_admin", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modaln_viewprogress_admin",
            is_open=False,
        ),
    dcc.Interval(
        id='interval-component',
        interval=5*1000, # in milliseconds
        n_intervals=0),
    dbc.Alert(id='tbl_outn'),
    dcc.Location( id='link_N_admin',href='',refresh=False)
])

#------------above is layoutnurse_for_admin--------below is layoutnuse_for_nurses---------#

layoutnurse_nurse= dbc.Container([
    html.H1(children='Nurses List'),
    dbc.Button("Administration Login",id='login_button',n_clicks=0,style={'margin-left':'86%','color':'#ed8413','background-color':'transparent','border':'none'}),
    html.Hr(),
    dt.DataTable(
        id='tbln_nurse',
        columns=[{"name": "Name", "id": "name"}, {"name": "Nurse ID", "id": "nurse_id"}, {"name": "Check in time", "id": "checkin_time"}, 
        {"name": "Status", "id": "status"},{"name": "Progress", "id": "progress_link"},{"name": "Patients", "id": "patient_link"}],
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
                    dcc.Interval(id="view_progress_nurse", n_intervals=0, interval=1*1000), #1ms
                    html.H3("Tasks", style={'marginLeft':'15px', 'font-weight': '400'}),
                    ]),
                    html.Hr(),
                    html.Br(),
            html.Div(id='task_checklist', children=[] ),
            dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_N_viewprogress_nurse", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modaln_viewprogress_nurse",
            is_open=False,
        ),
    dbc.Modal(
            [
            dbc.ModalBody([
                    login_page
                            ]),
            dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_login", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal_login",
            is_open=False,
        ),
    dcc.Interval(
        id='interval-component',
        interval=5*1000, # in milliseconds
        n_intervals=0),
    dbc.Alert(id='tbl_outn'),
    dcc.Location( id='link_N_nurse',href='',refresh=False)
])
#---------------above is nursetlayout_for_nurse--------------below is patientlayout--------------

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

dfp = pd.read_csv(DATA_PATH.joinpath("patientlist.csv"))

layoutpatient= dbc.Container([
    html.H1(children='Paitents List'),
    dbc.Button("Back",id="back_P",color="link", style={'margin-left': '-10px','background-color':'#eef2f6','color':'black', 'border':''},className="me-1",n_clicks=0),
    html.Br(),
    dbc.Button('Add New Patient', id='button_P',
    style={'display': 'inline-block','border':'none','background-color':'#eef2f6','color':'black','margin-left': '982px','height': '33px'}),
    dt.DataTable(
        id='tblp',
        columns=[{"name": "Name", "id": "name"}, {"name": "Patient ID", "id": "patient_id"},
        {"name": "Risk Score", "id": "risk_score"}, {"name": "View Dashboard", "id": "dashboard_link"}],
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
    dbc.Alert(id='tbl_outp'),
    dbc.Modal(
            [
                dbc.ModalBody(html.Embed(src='https://ktong2023.github.io/test/',height="500",width="470",style={'matgin-top':'400vw'})),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_P", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modalp",
            is_open=False,
        ),
    dcc.Interval(
        id='interval-component',
        interval=5*1000, # in milliseconds
        n_intervals=0
    ),
    dcc.Location( id='link_P',href='',refresh=False)
])

#---------------Patient_Dashboard_Below---------------#
#message shortcuts
shortcut1='Hi, you have an upcoming appointment'
shortcut2='Please complete the survey: https://padnim14.github.io/patient-survey/'
shortcut3='Your medicine is ready to pick up'

patientDashboard = html.Div([

    html.H1(id='patient_name',children=[], style={'text-align': 'left','margin-left': '2%'}),
    dcc.Link("Back to patients",href='/patients',refresh=True,style={'color':'black','text-align': 'left','margin-left': '2%'}),
    html.Br(),html.Hr(),
    dcc.Link("Schedule appointment",href='/appointment',style={'text-align': 'left','margin-left': '2%'}),
    dbc.Button('Send text message',id='send_sms',n_clicks=0,style={'text-align': 'left','margin-left': '2%','border':'none',"background":'#ffffff','color':'black'}),
    html.Hr(),
    html.Div([
                html.H4(id='patient_age',children=[], style={'text-align': 'left','margin-left': '2%'}),
    ],style={'display': 'inline-block', 'vertical-align': 'top','margin-left': '2%'}),
    html.Div(children=[
                        html.Embed(id='question',src="https://padnim14.github.io/patient-survey/" , 
                            width="700", height="400", style={'border':'1px silver solid'}) ], 
    style={'display': 'inline-block', 'margin-left': '51vw', 'margin-top': '-2%'}),
    html.Hr(style={'width':'90%','color':'black'}),
    html.Div(children=[
        dcc.Graph(id='plot_scatter',style={'display': 'inline-block'}),
        dcc.Graph(id='plot_bar',style={'display': 'inline-block'}) ],
        style={ 'vertical-align': 'top', 'margin-right': '0vw', 'margin-bottom': '3vh'}),
    dbc.Modal([
                dbc.ModalBody([
                    dbc.Container([
                                html.H3("Send text message", style={'padding':'5px'}),
                                html.Br(),
                                dcc.Dropdown(
                                    id='shortcuts',
                                    options=[
                                        {'label': shortcut1, 'value': shortcut1},
                                        {'label': shortcut2, 'value': shortcut2},
                                        {'label': shortcut3, 'value': shortcut3}
                                    ],
                                    placeholder='Select one short cut to send',
                                    style={'width':'100%','padding':'5px'}
                                ),
                                html.Br(),html.Br(),
                                dcc.Input(id='custom_txt',type="text", placeholder="Or send a custom message",debounce=True, 
                                persistence=False,style={'margin-left':'5px','width':'98%','padding':'10px'}),
                                html.Br(),html.Br(),html.Hr(),
                                dbc.Button("Send",id="send_message",n_clicks=0,style={'display': 'block','margin-left':'45%',}),
                                dcc.ConfirmDialog(
                                    id='confirmation_sms',
                                    message='Text message sent successfully',
                                )
                         ]),
                    ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_MC", className="ml-auto", n_clicks=0)
                ),
            ],
            id="MessageCenter",
            is_open=False,style={'width':'100%'}
        ),
    dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds
        n_intervals=0),
    dcc.Location( id='link_D',href='',refresh=False)
]) 

#--------------------Appoitment Page(Calendar)----------------------#
external_stylesheets = [dbc.themes.COSMO]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
layoutAppointment = dbc.Container(className="responsive", children=[
    html.Br(),
    dcc.Link("Back to Dashboard",href='/dashboard',refresh=True,style={'color':'black','text-align': 'left'}),
    html.Br(),html.Hr(),
    html.Embed(id='calendar',src="https://calendar.google.com/calendar/embed?src=hit2020fall%40gmail.com&ctz=America%2FIndiana%2FIndianapolis",
    style={'position':'','border': '0', 'width':'100%','height':'100vh','frameborder':'0', 'scrolling':'no'}),
    html.Hr(),
    html.H3("Schedule Appointment"),
    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=date(2019, 8, 5),
        max_date_allowed=date.today()+timedelta(days=365),
        initial_visible_month=date.today(),
        date=date.today()
    ),
    html.Br(),
    dcc.Input(
        id='start-time-input',
        type='time',
        placeholder="Start time", 
        size="sm",
        style={'margin-top':'2%','width':'20%'}
    ),
    html.Br(),
    dbc.Input(
        id='description',
        type='text',
        placeholder="Description for the appointment", 
        size="lg",
        style={'margin-top':'1px','width':'50%'}
    ),
    html.Div([dbc.Button("Confirm",id="confirmApp",n_clicks=0, style={'margin-top':'20px'}),]),
    dcc.ConfirmDialog(
        id='confirmation',
        message='Appointment successfully scheduled',
    ),

    html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
    dcc.Location(id='refresh',refresh=True)
])