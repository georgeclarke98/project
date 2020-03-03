The goal of this project is to produce a user friendly set of tools for producing engaging online history.
Try to produce a set of sites and apps working from the  “This Day In Labor History” corpus which:

1) presents the corpus in electronic calendar form
2) allows for the production of custom paper calendars derived from the corpus
(e.g., as offered by https://www.myphotobook.co.uk/photo-calendar or https://www.timeanddate.com/calendar/create.html )
3) presents the corpus in csv form (fixing various usability issues)
 
all while allowing fairly non technical people to contribute new articles and perspectives.
 
Update project steps:

1.cd /Users/jay/Desktop/callirhoe-master 
2.git status
3.git commit -a -m "tag"
4.git push
  
First step:
  
Open the file
$ cd file path
  
Second step:
  
Save the data extracted from the corpus into the database and export the data as a csv file:
$ python3 example.py
  
Third step:
  
Users can select desired images from the database and generate corresponding QRcode by inputting the image number:
$ python3 interface.py number1 number2
  
Fourth step:
  
Users can resize the image to match the size of the calendar
$ convert -resize 2828x1700! number.jpg number.jpg
  
Fifth step:
  
Users can add QR code to images
$ convert number.jpg number.png -gravity northeast -geometry +5+10 -composite outputmonthnumber.jpg
  
Sixth step:
  
Users can Stitch Images(with QR code) and calendars
$ convert -append outputmonthnumber.jpg calendarmonth.jpg finaloutputmonth.jpg