from bs4 import BeautifulSoup
import requests
import html_to_json
import re
from icalendar import Calendar, Event, vText
from datetime import datetime, timedelta
from pathlib import Path
import os
import pytz
import logging

EVENT_WEBPAGE_URL = "https://www.rcmusic.com/ggs/master-classes-and-performances/student-recitals-and-community-performances"

# setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def remove_escape_chars(table_json):
    """Removes escape characters and extra whitespace from a JSON object.

    Args:
        table_json (list): A list of dictionaries representing a table.

    Returns:
        list: The cleaned JSON object.
    """
    for row in table_json:
        for key in row:
            row[key] = re.sub(
                r'\s+', ' ', bytes(str(row[key]), 'utf-8').decode('utf-8'))
            row[key] = row[key].replace("\u200b", " ")
    return table_json


def parse_date(date_str):
    """Parses a date string and returns a datetime object.

    The function tries to parse the date string with multiple formats.
    If the year is not present in the date string, the current year is added before parsing.
    The timezone is set to 'America/Toronto'.

    Args:
        date_str (str): The date string to parse.

    Returns:
        datetime: The parsed datetime object.

    Raises:
        ValueError: If the date string does not match any of the supported formats.
    """
    current_year = datetime.now().year

    # If date string doesn't contain a year, add it
    # Check if year pattern (4 digits) exists in the string
    if not re.search(r'\b\d{4}\b', date_str):
        # Add year after the day number (e.g., "Friday, September 5" -> "Friday, September 5, 2025")
        # Match pattern: day of week, month name, day number, then rest
        date_str = re.sub(r'(\w+,\s+\w+\s+\d+)(\s+)', rf'\1, {current_year}\2', date_str)

    formats = ["%A, %B %d, %Y %I:%M%p", "%A, %B %d, %Y, %I:%M%p"]

    for fmt in formats:
        try:
            date = datetime.strptime(date_str, fmt).replace(
                tzinfo=pytz.timezone('America/Toronto'))
            return date
        except ValueError:
            continue
    raise ValueError(
        f"Date string '{date_str}' does not match any of the formats: {formats}")

def create_ics(table_json):
    """Creates an iCalendar file from a JSON object.

    The function creates an iCalendar file with all the concerts from the
    JSON object. The file is saved in the 'calendars' directory.

    Args:
        table_json (list): A list of dictionaries representing the concerts table.
    """
    cal = Calendar()
    cal.add('prodid', '-//The Royal Conservatory Student Recitals and Community Performances//www.rcmusic.com//')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('X-WR-CALNAME', 'The Royal Conservatory Concerts')
    cal.add('X-WR-TIMEZONE', 'America/Toronto')
    
    for entry in table_json:
        if not entry:
            continue
        event = Event()
        try:
            event.add('summary', entry['Artist & Discipline'])
            event['location'] = vText(entry['Location'])
            event.add('description', EVENT_WEBPAGE_URL)
            if 'Date & Time' in entry:
                start_time = parse_date(entry['Date & Time'])
            else:
                start_time = parse_date(f"{entry['Date']} {entry['Time']}")
        except KeyError:
            logger.error("KeyError: %s", entry)
        except ValueError:
            logger.error("ValueError: %s", entry)
        except Exception as e:
            logger.error("Unexpected error (%s): %s", e, entry)
            continue
        else:
            event.add('dtstart', start_time)
            event.add('dtend', start_time + timedelta(hours=1))
            cal.add_component(event)

    # Write to disk
    directory = Path.cwd() / 'calendars'
    directory.mkdir(parents=True, exist_ok=True)

    f = open(os.path.join(directory, 'all_concerts.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()


def main():
    """Fetches the concert data, parses it, and creates an iCalendar file.

    The main function that orchestrates the scraping, parsing, and iCalendar
    creation process.

    Returns:
        bool: True if the iCalendar file was created successfully, False otherwise.
    """
    try:
        response = requests.get(EVENT_WEBPAGE_URL)
        response.raise_for_status()  # Raises HTTPError for bad status codes (4xx, 5xx)
        html_doc = response.text
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error occurred while fetching the webpage: %s", e)
        print(f"Failed to fetch the webpage. HTTP error: {e}")
        return False
    except requests.exceptions.RequestException as e:
        logger.error("Request error occurred: %s", e)
        print(f"Failed to fetch the webpage. Request error: {e}")
        return False
    
    soup = BeautifulSoup(html_doc, 'html.parser')

    # Try multiple methods to find concert tables for robustness
    # Method 1: Find tables directly (current website structure)
    concert_tables = soup.find_all("table")

    rows = []
    if concert_tables:
        for table in concert_tables:
            rows.extend(table.find_all("tr"))

    # Method 2: Fallback to finding divs with class "rcm-responsive-table" (old structure)
    if not rows:
        concert_divs = soup.find_all("div", class_="rcm-responsive-table")
        if concert_divs:
            for div in concert_divs:
                rows.extend(div.find_all("tr"))

    if not rows:
        print("No concerts found on the webpage.")
        return False

    # Add table tag to the html (helps html_to_json to parse the table)
    table_html = "<table>\n"
    for row in rows:
        table_html += str(row)
    table_html += "\n</table>"

    # Convert the table_html to json
    # table_json is a list of dictionaries (each list is a row in the table)
    # Each dictionary has three keys: "Date & Time", "Location", and "Artist & Discipline"

    table_json = remove_escape_chars(
        html_to_json.convert_tables(table_html)[0])

    # Create the ics file
    create_ics(table_json)
    print("Successfully created the ics file.")
    return True


if __name__ == '__main__':
    # This block ensures that the main() function is called only when the script
    # is executed directly, not when it's imported as a module.
    main()
