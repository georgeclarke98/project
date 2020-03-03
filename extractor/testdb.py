import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
from PIL import Image
import qrcode
import re
# make the url variable
# for website which has more than one page
# url_page_2 = url + '&page=' + str(2) + '&s=relevance'
# def get_data_from_url(url,10):
# regard as the new function of my project
def saveToSqlite(calendar_info):
    # obtain history_info
    title = calendar_info['title']
    image = calendar_info['image']
    link = calendar_info['link']


    # connect to sqlite
    con = sqlite3.connect('history.db')
    cur = con.cursor()
    sql = "insert into calendar_info values ('%s', '%s', '%s')" % (title, image, link)
    try:
        cur.execute(sql)
    except:
        pass
    con.commit()

def grabsubpages():
    header1 = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    url = "http://www.lawyersgunsmoneyblog.com/2012/07/this-day-in-labor-history-a-years-retrospective"

    r = requests.get(url=url, headers = header1)

    soup = BeautifulSoup(r.content, 'lxml')

# print(r.content)
    test_title = {}
    number = 0
    titles = soup.select("div[class='admania_entrycontent'] a")
    for title in titles:
        test_title[number] = title.get_text()
        number += 1

    print(test_title)

    test_link = {}
    link_text = []
    image_c = []
    number = 0
    links = soup.select("div[class='admania_entrycontent'] a")  # CSS 选择器
    for link in links:  # Parse through each url in the list.
        test_link[number] = link.get('href')
        number += 1

    print(test_link)

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
        number += 1
        saveToSqlite(calendar_info)
#for item in list_data:
#    print (item.contents[2].text)
'''
titles = soup.select("div[class='admania_entrycontent'] a")   # CSS selector
for title in titles:
    print(title.get_text())    # for titles

links = soup.select("div[class='admania_entrycontent'] a")  # CSS 选择器
for link in links:
   print(link.get('href'))  # for links
'''
# download images for generating calenders
'''def DownloadImages():
    con = sqlite3.connect('history.db')
    cur = con.cursor()
    sql = "SELECT image FROM history_info"
    try:
        cur.execute(sql)
        Image_list = cur.fetchall()
    except:
        pass
    con.commit()

    print(Image_list[10][0])
    number = 0
    for number in range(len(Image_list)):
        url_image = Image_list[number][0]
        header1 = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        img = requests.get(url = url_image, headers = header1)
        f = open(str(number)+'.jpg','ab')
        f.write(img.content)
        f.close()
        number += 1
        if number == 13:
           break
'''
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


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    grabsubpages()
   # DownloadImages()
    readsqlite()
    endtime = datetime.datetime.now()
    print ("TIME: ", (endtime - starttime).seconds, "s")
