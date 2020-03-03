import requests
from bs4 import BeautifulSoup

# make the url variable
# for website which has more than one page
# url_page_2 = url + '&page=' + str(2) + '&s=relevance'
# def get_data_from_url(url,10):
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5e994bRvJ6YsZ_58keUG9rGr0NOc-NClh1eLtHHHqWrHn2FGGBB0kvXcoLWRzwg/pubhtml"
r = requests.get(url)

soup = BeautifulSoup(r.content)

soup.find_all("a")

g_data = soup.find_all("td", {"class": "s0"})

for item in g_data:
    print(item.text)

g1_data = soup.find_all("td", {"class": "s1"})

for item in g1_data:
   print(item.text)

g2_data = soup.find_all("td", {"class": "s2"})

for item in g2_data:
    print(item.contents[0])
