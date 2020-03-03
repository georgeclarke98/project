import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
import pandas
from PIL import Image
import qrcode
import re
# make the url variable
# for website which has more than one page
# url_page_2 = url + '&page=' + str(2) + '&s=relevance'
# def get_data_from_url(url,10):
# regard as the new_test function of my project

# Connect to the database by using the sqlite3 module
def saveToSqlite(calendar_info, firstTime):
    # obtain history_info
    title = calendar_info['title']
    image = calendar_info['image']
    link = calendar_info['link']


    # connect to sqlite
    con = sqlite3.connect('/Users/georgeclarke/Documents/Third_Year_Project/callirhoe/extra_sqlite/history.db')
    cur = con.cursor()

    if firstTime:
        cur.execute("delete from calendar_info")

    sql = "insert into calendar_info values ('%s', '%s', '%s')" % (title, image, link)
    try:
        cur.execute(sql)
    except:
        pass
    con.commit()

# extracting data from homepage and subpages by using beautifulsoup4
def grabsubpages():
    header1 = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
# input the url of the homepage
    url = "http://www.lawyersgunsmoneyblog.com/2012/07/this-day-in-labor-history-a-years-retrospective"

    r = requests.get(url=url, headers = header1)

    soup = BeautifulSoup(r.content, 'lxml')

# print(r.content)
    test_title = {}
    number = 0
# obtain titles of different articles from homepage
    titles = soup.select("div[class='admania_entrycontent'] a")
    for title in titles:
        test_title[number] = title.get_text()
        number += 1

    print(test_title)

    test_link = {}
    link_text = []
    image_c = []
    number = 0
    firstTime = True
    links = soup.select("div[class='admania_entrycontent'] a")  # CSS
    for link in links:  # Parse through each url in the list.
        test_link[number] = link.get('href')
        number += 1

    print(test_link)
# extracting images from subpages

    for i in range(len(test_link)):
        page = requests.get(url=test_link[i], headers = header1)

        soup = BeautifulSoup(page.content, 'lxml')

        try:

            image = soup.find('a', href=re.compile(r"uploads"))  # CSS 选择器
            image_url = image.contents[0]
            image_src = image_url.get('src')
            image_c.append(image_src)
            print(image_src)

            # print(image)  # for image
        except:
           print("image failure")
           image_c.append('null')
           pass

    for number in range(len(test_title)):
        calendar_info = {"title": test_title[number], "image": image_c[number],  "link":test_link[number]}
        saveToSqlite(calendar_info, firstTime)
        if number == 0:
            firstTime = False
        number += 1

# exporting table to csv file by using sqlite3 and pandas
def sqltocsv():
    con = sqlite3.connect('/Users/georgeclarke/Documents/Third_Year_Project/callirhoe/extra_sqlite/history.db')
    table = pandas.read_sql('select * from calendar_info', con)
    table.to_csv('/Users/georgeclarke/Documents/Third_Year_Project/callirhoe/extra_sqlite/output.csv')
'''
# download images for generating calenders
def DownloadImages():
    con = sqlite3.connect('history.db')
    cur = con.cursor()
    sql = "SELECT image FROM history_info"
    try:
        cur.execute(sql)
        Image_list = cur.fetchall()
    except:
        pass
    con.commit()

    # print(Image_list[10][0])

    for number in range(len(Image_list)):
        url_image = Image_list[number][0]
        header1 = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        img = requests.get(url = url_image, headers = header1)
        f = open(str(number)+'.jpg','ab')
        f.write(img.content)
        f.close()


# generate QRcode
def readsqlite():
    con = sqlite3.connect('history.db')
    cur = con.cursor()
    sql = "SELECT link FROM calendar_info"
    try:
        cur.execute(sql)
        link_list = cur.fetchall()
    except:
        pass
    con.commit()
    print(link_list[0][0])
    number = 0
    for number in range(len(link_list)):
        url_link = link_list[number][0]
        img=qrcode.make(url_link)
        img.save(str(number)+'.png')
        number += 1
        if number == 13:
           break
'''

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    grabsubpages()
    sqltocsv()
    # DownloadImages()
    # readsqlite()
    endtime = datetime.datetime.now()
    print ("TIME: ", (endtime - starttime).seconds, "s")
