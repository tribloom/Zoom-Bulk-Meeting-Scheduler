from datetime import datetime

from zoom_api_helper import ZoomAPI
from zoom_api_helper.models import *

# Based on https://github.com/rnag/zoom-api-helper#bulk-create-meetings
# Modified to add recurring meetings and use 24 hour time.
# i.e. 1600 is 4:00 PM, 1130 is 11:30 AM

def main():
    zoom = ZoomAPI('CLIENT_ID', 'CLIENT_SECRET', 'ACCOUNT_ID')

    # (optional) column header to keyword argument
    col_name_to_kwarg = {'Group Name': 'agenda',
                         'Zoom Username': 'host_email',
                         'Passcode': 'password'}

    # (optional) predicate function to initially process the row data
    def process_row(row: 'RowType', dt_format='%Y-%m-%d %H%M'):
        def rotate_weekday(day: int):
            if day <= 5:  # Saturday
                return day + 2
            elif day == 6:  # Sunday
                return 1

        start_time = f"{row['Meeting Date'][:10]} {row['Meeting Time']}"

        # See https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/meetingCreate
        if row['Number of Times to Meet'] and row['Number of Times to Meet'] != '' and row['Number of Times to Meet'].isdigit() and row['Number of Times to Meet'] != '1':
            recurrence_dict = {
                'end_times':  row['Number of Times to Meet'],
                'type': 2,  # weekly
                'weekly_days': str(rotate_weekday(datetime.strptime(start_time, dt_format).weekday()))  # Need to determine the day of the week of the initial meeting date (weekday() returns monday = 0, sunday = 6, zoom needs sunday = 1, saturday = 7)
            }
            row.update(
                start_time=datetime.strptime(start_time, dt_format),
                # Zoom expects the `duration` value in minutes.
                duration=int(row['Duration Hr']) * 60 + int(row['Duration Min']),
                recurrence=recurrence_dict,
                type=Meeting.RECURRING_WITH_TIME
            )
        else:
            hr = row['Duration Hr']
            mi = row['Duration Min']
            if hr == '':
                hr = 0
            else:
                hr = float(hr)
            if mi == '':
                mi = 0
            else:
                mi = float(mi)
            row.update(
                start_time=datetime.strptime(start_time, dt_format),
                # Zoom expects the `duration` value in minutes.
                duration=int(row['Duration Hr']) * 60 + int(row['Duration Min'])
            )
        return True

    # (optional) function to update row(s) with the API response
    def update_row(row: 'RowType', resp: dict):
        row['Meeting URL'] = resp['join_url']
        row['Meeting ID'] = resp['id']
        if 'password' in resp:
            row['Passcode'] = resp['password']

    # create meetings with dry run enabled.
    zoom.bulk_create_meetings(
        col_name_to_kwarg,
        excel_file='./meeting-info.xlsx',
        default_timezone='America/Denver',
        process_row=process_row,
        update_row=update_row,
        # comment out below line to actually create the meetings.
        # dry_run=True,
    )


if __name__ == '__main__':
    main()
