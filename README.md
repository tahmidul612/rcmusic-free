# rcmusic-free

A Python script that scrapes the Royal Conservatory of Music's website for free student recitals and community performances and generates an iCalendar (`.ics`) file. This allows you to easily add and stay updated with the latest free concert schedules in your favorite calendar application.

> [!NOTE]
> The public calendar is updated every hour. For real-time updates, subscribe to the calendar and enable event change notifications in your calendar app.

## Getting the Concert Calendar

You can easily subscribe to the concert calendar without running the script yourself.

[![Add to Google Calendar](https://img.shields.io/badge/Add_to_Google_Calendar-darkslategray?style=for-the-badge&logo=googlecalendar)](https://calendar.google.com/calendar/u/0?cid=ODkzZjEyYTRhMjQ1ZDIxZTZkYjZkOTk1NDc0ODRjNTlhZmYzYWY2MTA3MjlhMTY0ZTFmMTI1ODcyNjg1ZmZjZUBncm91cC5jYWxlbmRhci5nb29nbGUuY29t)

[![Get iCal File](https://img.shields.io/badge/Get_iCal_File-white?style=for-the-badge&logo=googlecalendar&logoColor=red)](https://rc-music-all.tahmidul612.workers.dev)

## How It Works

The `main.py` script performs the following steps:
1.  **Fetches HTML**: It sends an HTTP GET request to the [RCM's student recitals and community performances page](https://www.rcmusic.com/ggs/master-classes-and-performances/student-recitals-and-community-performances).
2.  **Parses HTML**: Using `BeautifulSoup`, it parses the HTML content and extracts the table containing the concert schedule.
3.  **Converts to JSON**: The extracted HTML table is converted into a JSON format for easier data manipulation.
4.  **Generates iCalendar file**: It iterates through the concert data, creating an iCalendar `Event` for each entry.
5.  **Saves the file**: The script saves the generated calendar as `calendars/all_concerts.ics`.

## Running the Script Locally

If you want to run the script yourself, follow these instructions.

### Prerequisites

*   Python 3.11 or higher

### Setup and Execution

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/rcmusic-free.git
    cd rcmusic-free
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate on Windows
    .\venv\Scripts\Activate.ps1

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the script:**
    ```bash
    python main.py
    ```
    This will create the `all_concerts.ics` file inside the `calendars` directory. You can then import this file into any calendar application that supports the iCalendar format (e.g., Google Calendar, Apple Calendar, Outlook).

> [!NOTE]
> An iCal file generated manually will not be updated automatically. You will need to run the script again and re-import it to your calendar app to get the latest schedule. To stay updated automatically, use the subscription links provided above.

[^1]: [Royal Conservatory of Music](https://www.rcmusic.com/ggs/master-classes-and-performances/student-recitals-and-community-performances)