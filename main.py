from bs4 import BeautifulSoup
import requests
def main():
    url = "https://www.rcmusic.com/ggs/master-classes-and-performances/student-recitals-and-community-performances"

    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')

if __name__ == '__main__':
    main()