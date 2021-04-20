from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from gui_config import AppGUI, gcal

# API Key:
# AIzaSyD0iMzDfjnSrUGwJRVeg9H0sZsR1Af014w

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_users_calendars(service):
    cals = {}
    calendar_list = service.calendarList().list().execute()
    for calendar in calendar_list['items']:
        # print(calendar['summary'], calendar['id'])
        cals[calendar['summary']] = calendar['id']
    return cals


def make_cal_pickle(service):
    if not os.path.exists('cal_res.pickle'):
        AppGUI().run()
        target_calendars = {}
        all_cals = get_users_calendars(service)
        for name in all_cals.keys():
            if 'Canvas' in name:
                target_calendars['Canvas'] = all_cals[name]
            else:
                for targ_cal in gcal:
                    if targ_cal.lower() in name.lower() and targ_cal is not '':
                        print(name, all_cals[name])
                        target_calendars[name] = all_cals[name]
        with open('cal_res.pickle', 'wb') as cf:
            pickle.dump(target_calendars, cf, pickle.HIGHEST_PROTOCOL)
            print('pickle made :)')
    return


def get_calendar_ids():
    with open('cal_res.pickle', 'rb') as cp:
        cal_dict =  pickle.load(cp)
        cal_list = [cal_dict['Canvas']]
        for key in cal_dict.keys():
            if 'Canvas' not in key:
                cal_list.append(cal_dict[key])
        return cal_dict

def main():
    service = authenticate()
    make_cal_pickle(service)
    cal_ids = get_calendar_ids()
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # Get all events from Canvas Calendar
    # TODO: Modify IDs for the different calendars you'd like to add to
    canvas = 'h355t080vd0c68l1qvfbgnbsrl86sis1@import.calendar.google.com'
    eecs312_id = 'umich.edu_1471sha5jmcn0knsebviui52i4@group.calendar.google.com'
    eng293_id = 'c_roua8kia7f9fli003agco5qgj8@group.calendar.google.com'
    phil110_id = 'umich.edu_nhuop1m0bg7slf5iiajt2maojk@group.calendar.google.com'
    soc344_id = 'umich.edu_8epjqpmk2vafdvaqemr64bbd08@group.calendar.google.com'
    # TODO: Change calendarId accordingly in below function call
    canvas_result = service.events().list(calendarId=cal_ids['Canvas'], timeMin=now, singleEvents=True,
                                            orderBy='startTime').execute()
    events = canvas_result.get('items', [])
    new_event_to_add = False
    if not events:
        print('No upcoming events found.')
    for event in events:
        # start = event['start'].get('dateTime', event['start'].get('date'))
        # print(start, event['summary'])
        title = event['summary']
        # TODO: Sub variables  in conditionals + 'cal_id' equivalencies
        cal_id = ''
        for key in cal_ids.keys():
            if key in title:
                cal_id = cal_ids[key]

        if cal_id == '':
            continue
        calendar_result = service.events().list(calendarId=cal_id, singleEvents=True,
                                                orderBy='startTime').execute()
        calendar_events = calendar_result.get('items', [])
        titles = []
        for e in calendar_events:
            titles.append(e.get('summary'))
        new_event = {
            'summary': event.get('summary'),
            'location': event.get('location'),
            'description': event.get('description'),
            'start': event.get('start'),
            'end': event.get('end'),
            'reminders': {
                "useDefault": True
            }
        }
        if event['summary'] not in titles:
            service.events().insert(calendarId=cal_id, body=new_event).execute()
            new_event_to_add = True
    if new_event_to_add:
        print("Events successfully added to Calendars!")
    else:
        print("No new events to add!")


if __name__ == '__main__':
    main()
