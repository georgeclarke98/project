import calmagick
import callirhoe
import lib
import os
import sys
import requests
import qrcode
import csv
import pandas
import random
import time
import urllib
import multiprocessing as mp
import argparse
import gooey

def readCSV(month, filename, mode):
    """
        Reads the csv file given as an input using pandas and return
        all the rows with events for the current month
    """
    #get all the rows for the current month
    reader = csv.DictReader(open(filename))
    rows = [row for row in reader if "/%02d/" % month in row["Date"] and row["Media"] != ""]

    writeHol = open("holidays/event.dat", "wb")

    if mode == "manual":
        #display options for manual mode
        count = 0
        for row in rows:
            print("\tOption " + str(count + 1) + ":")
            print("\t\t" + row["Title"])
            print("\t\tMedia Link: " + row["Media"])
            count = count + 1
        #get the choice from the user
        choice = raw_input("\n\t Please choose event for month " + str(month) + ": ")
        choiceNo = int(choice)
        while choiceNo > count or choiceNo < 1:
            choice = raw_input("\tInvalid choice, please choose a number between 1 and " +
                  str(count) + " for this month: ")
            choiceNo = int(choice)
        #return the chosen event
        date = rows[choiceNo-1]["Date"]
        writeHol.write("d|%02d%s|Event Today||normal\n" % (month, date[0:2]))
        writeHol.close()
        #create the event as a holiday so that it displays on the Date
        return rows[choiceNo - 1]
    else:
        row = random.choice(rows)
        date = row["Date"]
        writeHol.write("d|%02d%s|Event Today||normal\n" % (month, date[0:2]))
        writeHol.close()
        #create the event as a holiday so that it displays on the Date
        #return a random row from the month
        return row

def downloadImage(month, urlImage):
    """
        Downloads and saves the image for the given month
        from the given url
    """

    #gets the image content from the url
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    image = requests.get(urlImage, header)
    #create a file and save the contents of the image to it
    file = open("Events/Event" + str(month) + ".jpg", "wb")
    file.write(image.content)
    file.close()

def createQR(month, urlQr):
    """
        This generates a qr code based on the given link for the current
        month and saves it as qr(month).jpg so it can be stitched
        to the top half of the calendar
    """

    #saves the qr code from the given link for the given month
    qrImage = qrcode.make(urlQr)
    qrImage.save("Events/qr" + str(month) + ".png")

def createTop(month, currentPhoto, currentText, currentQR, title):
    """
        Create the top portion of the calendar, this stitches the current
        event image onto a self created background for the top half, then
        adds the text for that event next to the image. It then also adds
        the qr code for the
    """

    placement = month % 2
    #make the photo for the current month fit into a size suitable for
    #the calendar
    os.system("convert " + currentPhoto + " -resize 940x1000" +
             " Resources/resized" + str(month) + ".png")

    #combine the resized image with the background for the top
    os.system("convert Resources/background2.png Resources/resized" +
              str(month) + ".png -gravity west -geometry +" + str(20+(placement*940)) + "+25 " +
              "-composite Resources/outPhoto" + str(month) + ".jpg")

    if placement == 1:
        placement = 0
    else:
        placement = 1

    #use the text to add it to the photo
    os.system("convert Resources/outPhoto" + str(month) +
              ".jpg -gravity west -pointsize 40 -size 900x " +
              "caption:@" + currentText + " Resources/outputtext" + str(month) + ".jpg")
    os.system("convert Resources/outputtext" + str(month) + "-0.jpg Resources/outputtext" +
              str(month) + "-1.jpg -gravity northwest -geometry +" + str(20+(placement*960)) + "+150" +
              " -composite Resources/outputWithText" + str(month) + ".jpg")

    #Add the title to the top
    os.system("convert Resources/outputWithText" + str(month) + ".jpg -pointsize" +
              " 60 -size 1500x60 -fill purple1 -stroke purple1 -gravity North -draw " +
              "\"text 0,10 '"+ title + "'\" Resources/outputWithText" + str(month) + ".jpg")

    if placement == 1:
        placement = 0
    else:
        placement = 1

    #add the qr code to the calendar
    os.system("convert " + currentQR + " -resize 150x150 " + currentQR)
    os.system("convert Resources/outputWithText" + str(month) + ".jpg " +
    currentQR + " -gravity northeast -geometry +" + str(-5+(1780*placement)) + "-5 -composite " +
    "Resources/outputWithText" + str(month) + ".jpg")

def createPDF(CalendarName):
    """
        Append the top portion of the calendar to the calendar dates of
        the bottom part. Then create a new pdf of the calendar (if the
        current month is January), and add all the calendar months to the
        pdf
    """

    print("\tAdding to PDF")

    os.system("convert -compress none HistoryCalendar/Calendar* HistoryCalendar/Calendar.tiff")
    os.system("convert -compress jpeg HistoryCalendar/Calendar.tiff " + CalendarName + ".pdf")
    os.system("rm -r HistoryCalendar/Calendar.tiff")

    #combine all the months into one printable pdf file
    # if month == 1:
    #     os.system("convert HistoryCalendar/Calender" + str(month) +
    #             ".jpg " + CalendarName + ".pdf")
    # else:
    #     os.system("convert " + CalendarName + ".pdf HistoryCalendar/Calender" +
    #             str(month) + ".jpg " + CalendarName + ".pdf")
    return True

def createCal(month, monthInfo, background, CalendarName, CalendarTitle):
    """
        Creates the actual calendar
    """
    print("\tCreating Calendar components for month " + str(month))

    calmagick.main_program(background, month, True)
    #create the calendar of the current month

    downloadImage(month, monthInfo[month - 1]["Media"])
    createQR(month, monthInfo[month - 1]["Source URL"])
    #get the photo for that event and create qr code

    currentPhoto = "Events/Event" + str(month) + ".jpg"
    writeText = open("Events/Event" + str(month) + ".txt", "w")
    currentTextInfo = (monthInfo[month - 1]["Title"] + "\n\n" + monthInfo[month - 1]["Date"] +
                  "\n\n" + monthInfo[month - 1]["Description"])
    writeText.write(currentTextInfo)
    writeText.close()
    currentText = "Events/Event" + str(month) + ".txt"
    currentQR = "Events/qr" + str(month) + ".png"
    #get the saved event details

    createTop(month, currentPhoto, currentText, currentQR, CalendarTitle)
    #create the top part of the calendar with text, image
    #and qr code
    #combine the photo and text portion to the calendar for month

    os.system("convert -append Resources/outputWithText" + str(month) +
              ".jpg HistoryCalendar/HistoryCalendar" + str(month)
              + ".jpg HistoryCalendar/Calendar%02d.jpg" % month)

    return True


def main_program():
    CalendarName = raw_input("What would you like to call your calendar? " +
                   ("(Please ensure there are no spaces in the name e.g TestCalendar): "))
    titleChoice = raw_input("Would you like your own title? (y/n): ")
    while titleChoice != 'y' and titleChoice != 'n':
        titleChoice = raw_input("Please answer 'y' or 'n': ")
    if titleChoice == 'y':
        CalendarTitle = raw_input("What would you like the title of the calendar to be?: ")
    else:
        CalendarTitle = "The History Of Manchester"
    #Ask for thre name of the calendar and the title
    csvFile = raw_input("Please enter the location of your cvs file: ")

    #Option of choosing own background, so with a border etc.
    backgroundChoice = raw_input("Would you like to use your own background for the top? (y/n): ")
    while backgroundChoice != 'y' and backgroundChoice != 'n':
        backgroundChoice = raw_input("Please answer 'y' or 'n': ")
    if backgroundChoice == 'y':
        print("Reminder: The image must be of size 1920x1080!")
        background = raw_input("Please enter the location of the image: ")
    else:
        background = "Resources/background.jpg"

    modeChoice = raw_input("Would you like to manually choose events? (y/n): ")
    while modeChoice != "y" and modeChoice != "n":
        modeChoice = raw_input("Please choose 'y' or 'n': ")
    if modeChoice == "y":
        mode = "manual"
    else:
        mode = "random"
    #choose the mode

    monthInfo = []
    for month in range(1, 13):
        monthInfo.append(readCSV(month, csvFile, mode))

    pool = mp.Pool(mp.cpu_count())
    result = [pool.apply_async(createCal,args=(month, monthInfo, background, CalendarName, CalendarTitle)) for month in range(1,13)]
    pool.close()
    pool.join()
    #call the create calendar and parallelise the process
    #asynchronously apply the process for this part as nothing is shared

    createPDF(CalendarName)
    #Create the pdf from the indicudual components

if __name__ == "__main__":
    try:
        main_program()
    except lib.Abort as e:
        sys.exit(e.args[0])
