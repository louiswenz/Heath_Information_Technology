from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import datefinder
from datetime import datetime, timedelta

scopes = ['https://www.googleapis.com/auth/calendar']

#__run the commented lines first_#
# flow = InstalledAppFlow.from_client_secrets_file("client_secret_674336402509-5bfkedemco4bqu5dv74o3mqejos84mor.apps.googleusercontent.com.json", scopes=scopes)
# credentials = flow.run_console()
# pickle.dump(credentials, open("/Users/Louis/Desktop/VIP/Dashapp/apps/token.pkl","wb"))
#_________________#

credentials = pickle.load(open("token.pkl","rb"))
service = build("calendar","v3",credentials=credentials) 

#list calendar + save cal_id
cal_id = service.calendarList().list().execute()
cal_id = cal_id['items'][0]['id']
#get calendar event
eventlist = service.events().list(calendarId=cal_id).execute()
#create cal event
def create_event(start_time_str, summary, duration=1, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
    
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
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
    
create_event("15 December 9 PM", "Meeting")
