#coding=utf-8
import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
import qrcode
import argparse


# make the url variable
# for website which has more than one page
# url_page_2 = url + '&page=' + str(2) + '&s=relevance'
# def get_data_from_url(url,10):

    # obtain history_info    body = subpage_info['body']

    # connect to sqlite

parser = argparse.ArgumentParser(description='Users can select the  images and the QR code(generated from the link)according to the extracted article title, image and link')
parser.add_argument('-I', help="Image number-1 that you need. For example, if the number of the image is 11 in the database, you should input 10", nargs='+' ,type=int)
parser.add_argument('-Q', help="link number-1 that you need", nargs='+',type=int)
args = parser.parse_args()
I=args.I
Q=args.Q


def DownloadImages(I):
    con = sqlite3.connect('history.db')
    cur = con.cursor()
    sql = "SELECT image FROM calendar_info"
    try:
        cur.execute(sql)
        Image_list = cur.fetchall()
    except:
        pass
    con.commit()

    # print(Image_list[10][0])


    url_image = Image_list[I][0]
    header1 = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    img = requests.get(url = url_image, headers = header1)
    f = open(str(I)+'.jpg','ab')
    f.write(img.content)
    f.close()

def readsqlite(Q):
    con = sqlite3.connect('history.db')
    cur = con.cursor()
    sql = "SELECT link FROM calendar_info"
    try:
        cur.execute(sql)
        link_list = cur.fetchall()
    except:
        pass
    con.commit()
    url_link = link_list[Q][0]
    img=qrcode.make(url_link)
    img.save(str(Q)+'.png')

'''
url_image = "http://lawyersgunsmon.wpengine.com/wp-content/uploads/2011/07/uen_fea_grstrike_hrpr.jpg"
header1 = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
img = requests.get(url = url_image, headers = header1)
f = open('test.jpg','ab') #存储图片，多媒体文件需要参数b（二进制文件）
f.write(img.content) #多媒体存储content
f.close()'''

DownloadImages(I=5)
readsqlite(Q=5)
