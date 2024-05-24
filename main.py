from bs4 import BeautifulSoup
import requests
import html_to_json
import re
def remove_escape_chars(table_json):
    for row in table_json:
        for key in row:
            row[key] = re.sub('\s+', ' ', bytes(str(row[key]), 'utf-8').decode('utf-8'))
    return table_json
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
if __name__ == '__main__':
    main()