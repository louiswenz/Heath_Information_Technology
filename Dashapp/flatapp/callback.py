import dash
from dash.dependencies import Input, Output, State
import dash_table as dt
import pandas as pd
import pathlib
import plotly.express as px  
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from re import search
import webbrowser
from app import app
from firebase_admin import credentials
from firebase_admin import firestore
from layout import db,nurse_array,nurse_id_array,curr_nurse_id,patient_array,patient_id_array,curr_patient_id
from twilio.rest import Client
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import date,datetime, timedelta

token =0

#feeding data to patient list
@app.callback(Output('tblp', 'data'), Input('interval-component', 'n_intervals'))
def refresh_patient_table(interval):
    global curr_nurse_id
    global patient_id_array

    patient_id_array = []
    patient_array = []

    query = db.collection(u'nurses').document(curr_nurse_id).collection('patients').stream()

    for doc in query:
        patient_array.append(doc.to_dict())
        patient_id_array.append(doc.id)

    return patient_array

@app.callback(
    Output("modalp", "is_open"),
    [Input("button_P", "n_clicks"), Input("close_P", "n_clicks")],
    [State("modalp", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#link patientlist to patientDashboard and back button to nurselist
@app.callback(
    Output('link_P','href'),Output('link_P','refresh'),
    Input('back_P', 'n_clicks'),Input('tblp', 'active_cell') )
def patientlist_nav(n_clicks,active_cell):
    global token
    if n_clicks!=0:
        if token == 1:
            return ('/nurses-admin', True)
        else:
            return ('/nurses', True)
    if search("dashboard_link", str(active_cell)):
        global curr_patient_id
        curr_patient_id = patient_id_array[active_cell["row"]]
        return ('/dashboard/' + curr_nurse_id, True)

    else:
        return ('',False)


######--------------------------------------------------------patient^^^--nurse_below--------------######

#feeding data to nurse list
@app.callback(Output('tbln_nurse', 'data'), Input('interval-component', 'n_intervals'))
def refresh_nurse_table(interval):
    global nurse_id_array
    
    nurse_array = []
    nurse_id_array = []

    query = db.collection(u'nurses').stream()
    
    for doc in query:
        nurse_array.append(doc.to_dict())
        nurse_id_array.append(doc.id)

    return nurse_array

#modal_viewprogress_nurse open or close
@app.callback(
    Output('modaln_viewprogress_nurse', 'is_open'), Output('close_N_viewprogress_nurse', 'n_clicks'),Output('tbln_nurse', 'active_cell'),
    Input('tbln_nurse', 'active_cell'), Input("close_N_viewprogress_nurse", "n_clicks")
    ,[State("modaln_viewprogress_nurse", "is_open")])
def toggle_view_progress_nurse(active_cell, n2, is_open):
    if search("progress_link",str(active_cell))!=None or n2!=0:
        return (not is_open, 0,None)
    else:
        return ('',0,active_cell)


#-------------nurse_above-----dashboard_below----------------------------------#
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
    global curr_nurse_id
    global curr_patient_id

    #query = db.collection(u'nurses').document(u'B12v6a5o3dGXGId8g02j').collection('patients').document(u'00ovyLEhdfps05n58MtA')
    query = db.collection(u'nurses').document(curr_nurse_id).collection(u'patients').document(curr_patient_id)
    patientdata= query.get()
    #print(patientdata.to_dict())
    return (str(patientdata.to_dict().get('name')),
           "Age:" + str(patientdata.to_dict().get('age')) )

account_sid = 'AC18f4cc68aa19dffc73cf35a14b240990'
auth_token = '6bf7a8633d5c69f11314decadc9f3310'
client = Client(account_sid, auth_token)

#sending text message
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

@app.callback(
    Output('MessageCenter', 'is_open'), Output('close_MC', 'n_clicks'), Output('send_sms', 'n_clicks'),
    Input('send_sms', 'n_clicks'),Input('close_MC', 'n_clicks'),
    [State('MessageCenter', 'is_open')])
def toggle_Message_Center(send_sms_n_clicks, close_MC_n_clicks, is_open):
    if send_sms_n_clicks>0 or close_MC_n_clicks>0:
        return (not is_open, 0,0)
    else:
        raise dash.exceptions.PreventUpdate



#-----------------callback for login page----------------------------#

#layout_nurse_nav
@app.callback(
    Output('output1', 'children'),Output('link_N_nurse', 'href'),Output('link_N_nurse', 'refresh'),
   [Input('verify', 'n_clicks'),Input('tbln_nurse', 'active_cell')],
    state=[State('user', 'value'),
                State('passw', 'value')])
def layout_nurse_nav(n_clicks, active_cell,uname, passw):
    if search("patient_link", str(active_cell)):
        global curr_nurse_id
        curr_nurse_id = nurse_id_array[active_cell["row"]]
        return ('','/patients/' + curr_nurse_id, True)
    pw_pair={'abc':'123'}     #PASSWORD dict
    if uname =='' or uname == None or passw =='' or passw == None:
        return ('','',False)
    if uname not in pw_pair:
        return ('Incorrect Username','',False)
    if pw_pair[uname]==passw:
        global token
        token=1
        return ('Access Granted!','/nurses-admin',True)
    else:
        return ('Incorrect Password','',False)

#modal_login open or close
@app.callback(
    Output('modal_login', 'is_open'), Output('close_login', 'n_clicks'),Output('login_button', 'n_clicks'),
    Input('login_button', 'n_clicks'), Input("close_login", "n_clicks")
    ,[State("modal_login", "is_open")])
def toggle_modal(loginbutton_n_clicks, n2, is_open):
    if loginbutton_n_clicks>0 or n2!=0:
        return (not is_open, 0,0)
    else:
        return ('',0,0)
#---------call back for nurselayout_admin------------$
@app.callback(Output('tbln_admin', 'data'), Input('interval-component', 'n_intervals'))
def refresh_nurse_table(interval):
    global nurse_id_array
    
    nurse_array = []
    nurse_id_array = []

    query = db.collection(u'nurses').stream()
    
    for doc in query:
        nurse_array.append(doc.to_dict())
        nurse_id_array.append(doc.id)

    return nurse_array
#nurselayout_admin nav
@app.callback(Output('link_N_admin', 'href'), 
              Output('link_N_admin', 'refresh'),
              Input('tbln_admin', 'active_cell'),Input('signout_button', 'n_clicks'))
def nurse_admin_nav(active_cell,n_clicks):
    global token
    if search("patient_link", str(active_cell)):
        global curr_nurse_id
        curr_nurse_id = nurse_id_array[active_cell["row"]]
        return ('/patients/' + curr_nurse_id, True)
    #signout
    if n_clicks>0:
        token = 0
        return ('/nurses',True)
    else:
        return ('',False)

#viewprogress_nurse and create_task_nurse open or close in admin
@app.callback(
    Output('modaln_viewprogress_admin', 'is_open'),Output('modaln_admin', 'is_open'), Output('close_N_view_admin', 'n_clicks'),Output('tbln_admin', 'active_cell'), Output('close_N_admin', 'n_clicks'),
    Input('tbln_admin', 'active_cell'), Input("close_N_view_admin", "n_clicks"),Input("close_N_admin", "n_clicks")
    ,[State("modaln_viewprogress_admin", "is_open")],[State("modaln_admin", "is_open")])
def toggle_view_progress_nurse(active_cell, n2, n_clicks_close_N_admin, is_open, is_open_modaln_admin):
    if search("progress_link",str(active_cell))!=None or n2!=0:
        return (not is_open,is_open_modaln_admin, 0,None,0)
    if search("create_task",str(active_cell))!=None or n_clicks_close_N_admin!=0:
        return (is_open, not is_open_modaln_admin, 0, None,0)
    else:
        raise dash.exceptions.PreventUpdate


#for adding tasks in modal window
@app.callback(
    Output('task_checklist_admin','children'),Output('submit_task_admin','n_clicks'),Output('tasknameinput_admin','n_submit'),
    Input('submit_task_admin','n_clicks'),Input('tasknameinput_admin','value'), Input('tasknameinput_admin','n_submit'),Input('create_task_interval_admin','n_interval'),
    [State('task_checklist_admin','children')])
def more_output(n_clicks,value,n_submit,prevContent,n_interval): 
    if n_clicks==0 and n_submit==0:
        raise dash.exceptions.PreventUpdate
    elif n_clicks>0 or str(n_submit)!='0':
        if value is not None and len(str(value).strip())!=0:
            return ( prevContent +   [html.Div(children=[dbc.Checklist(options=[{'label': " "+str(value),'value':str(value)}], persisted_props=['value'], persistence=True, persistence_type='session',
                 style={'marginLeft':'15px','font-weight':''} ) ])], 0,0)
        else:return ( prevContent , 0,0)

#--------------------Appoitment Page(Calendar)----------------------#
scopes = ['https://www.googleapis.com/auth/calendar']

#__run the commented lines independently to get access token_#

#flow = InstalledAppFlow.from_client_secrets_file("client_secret_674336402509-5bfkedemco4bqu5dv74o3mqejos84mor.apps.googleusercontent.com.json", scopes=scopes)
#credentials = flow.run_console()
#pickle.dump(credentials, open("token.pkl","wb"))

#--------------------------------#

credentials = pickle.load(open("token.pkl","rb"))
service = build("calendar","v3",credentials=credentials) 

#create cal event
def create_event(start_time_str, summary, duration=1, description=None, location=None):
    start_time = datetime.strptime(start_time_str,"%Y-%m-%d %H:%M")
    end_time = start_time + timedelta(hours=duration)
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:00"),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:00"),
            'timeZone': 'America/New_York',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    
    return service.events().insert(calendarId='primary', body=event).execute()
@app.callback(
    Output('confirmation', 'displayed'),Output("confirmApp", "n_clicks"),Output("refresh", "href"),
    Input('my-date-picker-single', 'date'), Input("start-time-input", "value"), Input("confirmApp", "n_clicks"),Input('description','value'))
def makeappoint(date,time, n_clicks, description):
    string_prefix = 'You have selected: '
    if (date is not None) & (time is not None)&(n_clicks>0) & (description is not None):
        create_event(str(date)+" "+time,description)
        return (True, 0, '/appointment')
    else:
        raise dash.exceptions.PreventUpdate