# rcmusic-free

Get schedule for free concerts from the Royal Conservatory of Music in Toronto in you calendar[^1]

> [!NOTE]
> The calendar is updated every hour. Add event change notifications from your calendar app to get notified about the latest updates.

[![Add to Google Calendar](https://img.shields.io/badge/Add_to_Google_Calendar-darkslategray?style=for-the-badge&logo=googlecalendar)](https://calendar.google.com/calendar/u/0?cid=ODkzZjEyYTRhMjQ1ZDIxZTZkYjZkOTk1NDc0ODRjNTlhZmYzYWY2MTA3MjlhMTY0ZTFmMTI1ODcyNjg1ZmZjZUBncm91cC5jYWxlbmRhci5nb29nbGUuY29t)

[![Get iCal File](https://img.shields.io/badge/Get_iCal_File-white?style=for-the-badge&logo=googlecalendar&logoColor=red)](https://rc-music-all.tahmidul612.workers.dev)

## Build and Deploy Instructions

> Only if you want to run the code yourself

### Prerequisites

- Python 3.11

### Setup

- Clone the repository (or fork and clone)
- Create a virtual environment
  
    ```console
    python -m venv venv
    ```

- Activate the virtual environment

    ```console
    .\venv\Scripts\Activate.ps1 # For Windows
    ```

    ```console
    source venv/bin/activate # For Linux
    ```

- Install requirements

    ```console
    pip install -r requirements.txt
    ```

### Run

Running the `main.py` file will generate `all_concerts.ics` file in a folder named `calendars`. You can import this file to your calendar app.

```console
python main.py
```

> [!NOTE]
> iCal file generated manually is not updated automatically. You will have to run the script again and import it to your calendar app to get the latest schedule.

[^1]: [Royal Conservatory of Music](https://www.rcmusic.com/ggs/master-classes-and-performances/student-recitals-and-community-performances)
