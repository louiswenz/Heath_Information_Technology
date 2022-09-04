import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import date,datetime, timedelta
from dash.dependencies import Input, Output
import dash_core_components as dcc

scopes = ['https://www.googleapis.com/auth/calendar']

#__run the commented lines first_#

#flow = InstalledAppFlow.from_client_secrets_file("client_secret_674336402509-5bfkedemco4bqu5dv74o3mqejos84mor.apps.googleusercontent.com.json", scopes=scopes)
#credentials = flow.run_console()
#pickle.dump(credentials, open("token.pkl","wb"))

#--------------------------------#

credentials = pickle.load(open("token.pkl","rb"))
service = build("calendar","v3",credentials=credentials) 

#list calendar + save cal_id
# cal_id = service.calendarList().list().execute()
# cal_id = cal_id['items'][0]['id']
# #get calendar event
# eventlist = service.events().list(calendarId=cal_id).execute()
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

external_stylesheets = [dbc.themes.COSMO]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = dbc.Container(className="responsive", children=[
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
    dbc.Input(
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

@app.callback(
    Output('confirmation', 'displayed'),Output("confirmApp", "n_clicks"),Output("refresh", "href"),
    Input('my-date-picker-single', 'date'), Input("start-time-input", "value"), Input("confirmApp", "n_clicks"),Input('description','value'))
def makeappoint(date,time, n_clicks, description):
    string_prefix = 'You have selected: '
    if (date is not None) & (time is not None)&(n_clicks>0) & (description is not None):
        print(description)
        create_event(str(date)+" "+time,description)
        return (True, 0, '/')
    else:
        raise dash.exceptions.PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)