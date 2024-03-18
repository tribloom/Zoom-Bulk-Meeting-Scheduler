# Zoom-Bulk-Meeting-Scheduler

Based on https://github.com/rnag/zoom-api-helper#bulk-create-meetings

Modified to add recurring meetings and use 24 hour time,
 i.e. 1600 is 4:00 PM, 1130 is 11:30 AM.

Bulk schedule meetings in Zoom based on an Excel file.

Usage:

```
$ python bulk_scheduler.py
```

Note: Excel file should be named 'meeting-info.xlsx' and be in the same directory as bulk-meetings.py.

Example Excel Data:

| Agenda     |                   |         |              |              |             |              |             |            |          |                         |
| ---------- | ----------------- | ------- | ------------ | ------------ | ----------- | ------------ | ----------- | ---------- | -------- | ----------------------- |
| Group Name | Zoom Username     | Topic   | Meeting Date | Meeting Time | Duration Hr | Duration Min | Meeting URL | Meeting ID | Passcode | Number of Times to Meet |
| Agenda 1   | <zoom user email> | topic 1 | 2/22/2024    | 1600         | 0           | 90           |             |            | 1234     | 1                       |
| Agenda 2   | <zoom user email> | topic 2 | 2/22/2024    | 1130         | 1           | 30           |             |            |          | 2                       |

Note: Duration Hr just have a value.