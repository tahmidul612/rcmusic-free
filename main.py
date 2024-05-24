from bs4 import BeautifulSoup
import requests
import html_to_json
import re
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime, timedelta
from pathlib import Path
import os
import pytz


def remove_escape_chars(table_json):
    for row in table_json:
        for key in row:
            row[key] = re.sub('\s+', ' ', bytes(str(row[key]), 'utf-8').decode('utf-8'))
    return table_json

def create_ics(table_json):
    cal = Calendar()
    cal.add('prodid', '-//The Royal Conservatory Student Recitals//www.rcmusic.com//')
    cal.add('version', '2.0')
    for entry in table_json:
        event = Event()
        event.add('summary', entry['Artist & Discipline'])
        event['location'] = vText(entry['Location'])
        start_time = datetime.strptime(entry['Date & Time'], '%A, %B %d %I:%M%p').replace(tzinfo=pytz.timezone('America/Toronto')).replace(year=datetime.now().year)
        event.add('dtstart', start_time)
        event.add('dtend', start_time + timedelta(hours=1))
        cal.add_component(event)

    # Write to disk
    directory = Path.cwd() / 'calendars'
    try:
        directory.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("Folder already exists")
    else:
        print("Folder was created")

    f = open(os.path.join(directory, 'all_concerts.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()

def main():
    url = "https://www.rcmusic.com/ggs/master-classes-and-performances/student-recitals-and-community-performances"

    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Add table tag to the html (helps html_to_json to parse the table)
    table_html = "<table>\n"
    # Find ar tr (table row) tags and add them to the table_html
    for row in soup.find_all("tr"):
        table_html += str(row)
    table_html += "\n</table>"

    # Convert the table_html to json
    # table_json is a list of dictionaries (each list is a row in the table)
    # Each dictionary has three keys: "Date & Time", "Location", and "Artist & Discipline"

    table_json = remove_escape_chars(html_to_json.convert_tables(table_html)[0])
    
    # Create the ics file
    create_ics(table_json)

if __name__ == '__main__':
    main()