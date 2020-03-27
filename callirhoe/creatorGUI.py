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
from gooey import Gooey, GooeyParser
from subprocess import Popen, PIPE

def fontChoices():
    reader = csv.DictReader(open("Resources/fonts.csv"))
    fonts =  [row["Font"] for row in reader]
    return fonts

def get_parser():
    """
        Get the argument parser for requirements
    """

    parser = GooeyParser(description="A simple calendar creator for a historical corpus")
    #create the parser
    parser.add_argument("CSVFile", help="Location of the CSV file of events",
                        widget='FileChooser', default="Events/events.csv")
    parser.add_argument("CalendarName", help="Filename of the calendar (no spaces or file format at the end) e.g. TestCalendar")
    parser.add_argument("-t", "--title", default="The History of Manchester",
                        help="Choose your own calendar title")
    parser.add_argument("-b", "--background", default="Resources/background2.png",
                        help="Location of a background you wish to use for the top (must be 1920x1080)",
                        widget='FileChooser')
    parser.add_argument("-m", "--mode", choices=["random", "manual"], widget='Dropdown',
                        help="Sets the mode for choosing historical events")
    parser.add_argument("-c", "--category", widget='Dropdown', default="All",
                        choices=["All", "Art", "Conflict", "Construction", "Science & Technology", "Sport", "Transport", "University of Manchester"],
                        help="Choose a category of events to use in the calendar")
    parser.add_argument("-f", "--font", widget='Dropdown', default="Helvetica",
                        help="Choose the font you would like to use for the event",
                        choices=fontChoices())
    return parser

def readCSV(filename, mode, category):
    """
        Reads the csv file given as an input using pandas and return
        all the rows with events for the current month
    """
    #get all the rows for the current month

    events = []
    writeHol = open("holidays/event.dat", "a")

    if mode == "manual":
        os.system("cp -r " + filename + " current.csv")
        os.system("python3 selector.py")
        # PYTHON_PATH = sys.executable
        # process = Popen([PYTHON_PATH, 'selector.py'], stdout=PIPE, stderr=PIPE)
        # output, error = process.communicate()
        rows = csv.DictReader(open("eventsSelected.csv"))
        events = [row for row in rows]
        #Add all the chosen events to the monthInfo
        os.system("rm -r current.csv eventsSelected.csv")
        month = 1
        for row in events:
            date = row["Date"]
            writeHol.write("d|%02d%s|Event Today||normal\n" % (month, date[0:2]))
            #create the event as a holiday so that it displays on the Date
            #return a random row from the month
            month = month + 1
    else:
        for month in range(1,13):
            reader = csv.DictReader(open(filename))
            #Open the file to be read
            if category == 'All':
                rows = [row for row in reader if "/%02d/" % month in row["Date"] and row["Media"] != ""]
                #Choose from all possible if no category is chosen
            else:
                rows = [row for row in reader if "/%02d/" % month in row["Date"] and row["Media"] != "" and category in row["Tag"]]
                #Choose from that month all those in the category chosen
                if len(rows) == 0:
                    reader = csv.DictReader(open(filename))
                    rows = [row for row in reader if "/%02d/" % month in row["Date"] and row["Media"] != ""]
                    #Choose all possible ones in the month if theres none for that category in that month
            events.append(random.choice(rows))
            date = row["Date"]
            writeHol.write("d|%02d%s|Event Today||normal\n" % (month, date[0:2]))
            #create the event as a holiday so that it displays on the Date
            #return a random row from the month

    writeHol.close()
    return events

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

def createTop(month, currentPhoto, currentText, currentQR, title, background, font):
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
    os.system("convert " + background + " Resources/resized" +
              str(month) + ".png -gravity west -geometry +" + str(20+(placement*940)) + "+25 " +
              "-composite Resources/outPhoto" + str(month) + ".jpg")

    if placement == 1:
        placement = 0
    else:
        placement = 1

    #use the text to add it to the photo
    os.system("convert Resources/outPhoto" + str(month) +
              ".jpg -gravity west -font '" + font + "' -pointsize 40 -size 900x " +
              "caption:@" + currentText + " Resources/outputtext" + str(month) + ".jpg")
    os.system("convert Resources/outputtext" + str(month) + "-0.jpg Resources/outputtext" +
              str(month) + "-1.jpg -gravity northwest -geometry +" + str(20+(placement*960)) + "+150" +
              " -composite Resources/outputWithText" + str(month) + ".jpg")

    #Add the title to the top
    os.system("convert Resources/outputWithText" + str(month) + ".jpg -font '" + font + "' -pointsize" +
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

def createCal(month, monthInfo, background, CalendarName, CalendarTitle, backgroundTop, font):
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

    createTop(month, currentPhoto, currentText, currentQR, CalendarTitle, backgroundTop, font)
    #create the top part of the calendar with text, image
    #and qr code
    #combine the photo and text portion to the calendar for month

    os.system("convert -append Resources/outputWithText" + str(month) +
              ".jpg HistoryCalendar/HistoryCalendar" + str(month)
              + ".jpg HistoryCalendar/Calendar%02d.jpg" % month)

    return True

@Gooey
def main():
    parser = get_parser()
    args = parser.parse_args()
    #parse the arguments to get the settings

    CalendarName = args.CalendarName
    csvFile = args.CSVFile
    backgroundTop = args.background
    CalendarTitle = args.title
    mode = args.mode
    category = args.category
    font = args.font
    #apply the parsed arguments

    monthInfo = []
    background = "Resources/background.jpg"

    monthInfo = readCSV(csvFile, mode, category)
    #Get the events either randomly or manually

    pool = mp.Pool(mp.cpu_count())
    result = [pool.apply_async(createCal,args=(month, monthInfo, background, CalendarName, CalendarTitle, backgroundTop, font)) for month in range(1,13)]
    pool.close()
    pool.join()
    #call the create calendar and parallelise the process
    #asynchronously apply the process for this part as nothing is shared

    createPDF(CalendarName)
    #Create the pdf from the indicudual components
    os.system("rm -r holidays/event.dat")

if __name__ == "__main__":
    try:
        main()
    except lib.Abort as e:
        sys.exit(e.args[0])
