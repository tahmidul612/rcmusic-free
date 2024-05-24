from bs4 import BeautifulSoup
import requests
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
if __name__ == '__main__':
    main()