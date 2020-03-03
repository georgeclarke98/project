#coding=utf-8
import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
import qrcode
#import argparse
import sys

# this python script is used for downloading images and generating qrcode

    # obtain history_info    body = subpage_info['body']

    # connect to sqlite
'''parser = argparse.ArgumentParser(description='Users can select the  images and the QR code(generated from the link)according to the extracted article title, image and link')
parser.add_argument('-I', help="Image number-1 that you need. For example, if the number of the image is 11 in the database, you should input 10", nargs='+', type=int)
parser.add_argument('-Q', help="link number-1 that you need", nargs='+',type=int)
args = parser.parse_args()
I=args.I
Q=args.Q'''
# description of this tool
def command_line(cmd_line):
    re_cmd = []
    if cmd_line[1] == "--help":
        print("The goal of this project is to produce a user friendly set of tools for producing engaging online history")
        print("  ")
        print("Allows for the production of custom paper calendars derived from the corpus")
        print("Offered by https://www.myphotobook.co.uk/photo-calendar or https://www.timeanddate.com/calendar/create.html")
        print("  ")
        print("Presents the corpus in csv form (fixing various usability issues)")
        print("  ")
        print("==========================================================================================")
        print("  ")
        print("First step:")
        print("  ")
        print("Open the file")
        print("$ cd file path")
        print("  ")
        print("Second step:")
        print("  ")
        print("Save the data extracted from the corpus into the database and export the data as a csv file:")
        print("$ python3 example.py")
        print("  ")
        print("Third step:")
        print("  ")
        print("Users can select desired images from the database and generate corresponding QRcode by inputting the image number:")
        print("$ python3 interface.py number1 number2")
        print("  ")
        print("Fourth step:")
        print("  ")
        print("Users can resize the image to match the size of the calendar")
        print("$ convert -resize 2828x1700! number.jpg number.jpg")
        print("  ")
        print("Fifth step:")
        print("  ")
        print("Users can add QR code to images")
        print("$ convert number.jpg number.png -gravity northeast -geometry +5+10 -composite outputmonthnumber.jpg")
        print("  ")
        print("Sixth step:")
        print("  ")
        print("Users can Stitch Images(with QR code) and calendars")
        print("$ convert -append outputmonthnumber.jpg calendarmonth.jpg finaloutputmonth.jpg")
        return 0
    elif len(cmd_line) == 1:
        return 0
    else:
        for j in range(len(cmd_line)-1):
            re_cmd.append(int(cmd_line[j+1]))
    return re_cmd

# download images for generating calenders
def DownloadImages(x):
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

    for i in range(len(x)):
        I = x[i]
        url_image = Image_list[I][0]
        header1 = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        img = requests.get(url = url_image, headers = header1)
        f = open(str(I)+'.jpg','ab')
        f.write(img.content)
        f.close()
# generate QRcode
def readsqlite(y):
    con = sqlite3.connect('history.db')
    cur = con.cursor()
    sql = "SELECT link FROM calendar_info"
    try:
        cur.execute(sql)
        link_list = cur.fetchall()
    except:
        pass
    con.commit()
    for i in range(len(y)):
        Q = y[i]
        url_link = link_list[Q][0]
        img=qrcode.make(url_link)
        img.save(str(Q)+'.png')

'''
url_image = "http://lawyersgunsmon.wpengine.com/wp-content/uploads/2011/07/uen_fea_grstrike_hrpr.jpg"
header1 = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
img = requests.get(url = url_image, headers = header1)
f = open('test.jpg','ab') ）
f.write(img.content) #
f.close()'''
c = sys.argv
cl = command_line(c)
if cl != 0:
    DownloadImages(cl)
    readsqlite(cl)
