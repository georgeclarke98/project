import unittest2 as unittest
import warnings
import creatorGUI
import os
import requests
from PIL import Image

def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test

class TestFontChoices(unittest.TestCase):
    @ignore_warnings
    def testGetsFonts(self):
        """
           Tests that a list is returned and is not empty
        """
        fonts = creatorGUI.fontChoices()
        self.assertTrue(fonts)

    @ignore_warnings
    def testFontsContent(self):
        """
           Tests the contents of the returned list
        """
        fonts = creatorGUI.fontChoices()
        self.assertEquals(fonts, ['AvantGarde-Book', 'AvantGarde-BookOblique',
        'AvantGarde-Demi', 'AvantGarde-DemiOblique', 'Bookman-Demi', 'Bookman-DemiItalic',
        'Bookman-Light', 'Bookman-LightItalic', 'Courier', 'Courier-Bold',
        'Courier-BoldOblique', 'Courier-Oblique', 'fixed', 'Helvetica',
        'Helvetica-Bold', 'Helvetica-BoldOblique', 'Helvetica-Narrow',
        'Helvetica-Narrow-Bold', 'Helvetica-Narrow-BoldOblique', 'Helvetica-Narrow-Oblique',
        'Helvetica-Oblique', 'NewCenturySchlbk-Bold', 'NewCenturySchlbk-BoldItalic',
        'NewCenturySchlbk-Italic', 'NewCenturySchlbk-Roman', 'Palatino-Bold',
        'Palatino-BoldItalic', 'Palatino-Italic', 'Palatino-Roman', 'Symbol',
        'Times-Bold', 'Times-BoldItalic', 'Times-Italic', 'Times-Roman'])

class TestGetParser(unittest.TestCase):
    @ignore_warnings
    def testParserCreated(self):
        """
           Test that a parser is created and returned
        """
        parser = creatorGUI.get_parser()
        self.assertTrue(parser)

class TestReadCSV(unittest.TestCase):
    @ignore_warnings
    def testRandom(self):
        """
           tests that the4 write events are gathered from a test csvFile
        """
        events = creatorGUI.readCSV("Events/TestRead.csv", "random", "all")
        self.assertEquals(events, [{'Description': 'B of the Bang was a sculpture by Thomas Heatherwick next to the City of Manchester Stadium in Manchester, England, which was commissioned to mark the 2002 Commonwealth Games; it was one of the tallest structures in Manchester and the tallest sculpture in the UK until the completion of Aspire in 2008. It was taller and leaned at a greater angle than the Leaning Tower of Pisa. The sculpture took its name from a quotation of British sprinter Linford Christie, in which he said that he started his races not merely at the "bang" of the starting pistol, but at "the B of the Bang".\n', 'Title': 'Britain\'s tallest self-supporting sculpture, the "B of the Bang", is unveiled in Manchester', 'Media': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/B_of_the_Bang_%28landscape%29.jpg/500px-B_of_the_Bang_%28landscape%29.jpg', 'Source URL': 'https://en.wikipedia.org/wiki/B_of_the_Bang', 'Tag': 'Art', 'Place': 'Manchester', 'Location': '53.481721, -2.199870', 'Date': '12/01/2005'}, {'Description': ' Manchester United F.C. play their first game at Old Trafford. Old Trafford (/\xcb\x88tr\xc3\xa6f\xc9\x99rd/) is a football stadium in Old Trafford, Greater Manchester, England, and the home of Manchester United. With a capacity of 74,879, it is the largest club football stadium (and second largest football stadium overall after Wembley Stadium) in the United Kingdom, and the eleventh-largest in Europe. It is about 0.5 miles (800 m) from Old Trafford Cricket Ground and the adjacent tram stop.', 'Title': 'First game on Old Trafford', 'Media': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Manchester_United_Panorama_%288051523746%29.jpg/500px-Manchester_United_Panorama_%288051523746%29.jpg', 'Source URL': 'https://en.wikipedia.org/wiki/Old_Trafford', 'Tag': 'Sport', 'Place': 'Manchester', 'Location': '53.463199, -2.291276', 'Date': '19/02/1910'}, {'Description': 'The Whitworth Hall on Oxford Road and Burlington Street in Chorlton-on-Medlock, Manchester, England, is part of the University of Manchester. It has been listed Grade II* since 18 December 1963. The Gothic revival hall lies at the south-east range of the Old Quadrangle of the University, with the Manchester Museum adjoined to the north, and the former Christie Library connected to the west.', 'Title': 'The Whitworth Hall is opened by the Prince of Wales', 'Media': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Whitworth_Hall_Manchester.jpg/480px-Whitworth_Hall_Manchester.jpg', 'Source URL': 'https://en.wikipedia.org/wiki/Whitworth_Hall', 'Tag': 'Construction', 'Place': 'Manchester', 'Location': '53.465339, -2.233155', 'Date': '12/03/1902'}, {'Description': 'The Manchester Mark 1 was one of the earliest stored-program computers, developed at the Victoria University of Manchester from the Manchester Baby (operational in June 1948). It was also called the Manchester Automatic Digital Machine, or MADM. Work began in August 1948, and the first version was operational by April 1949; a program written to search for Mersenne primes ran error-free for nine hours on the night of 16/17 June 1949.', 'Title': 'The Manchester Mark 1 computer is operable at the University of Manchester', 'Media': 'https://upload.wikimedia.org/wikipedia/en/d/d8/Manchester_Mark2.jpg', 'Source URL': 'https://en.wikipedia.org/wiki/Manchester_Mark_1', 'Tag': 'Science & Technology', 'Place': 'Manchester', 'Location': '53.467035, -2.233878', 'Date': '01/04/1949'}, {'Description': 'Opened as Store Street in 1842, it was renamed Manchester London Road in 1847 and Manchester Piccadilly in 1960. Located to the south-east of Manchester city centre, it hosts long-distance intercity and cross-country services to national destinations including London, Birmingham, Glasgow, Edinburgh, Cardiff, Bristol, Exeter, Plymouth, Reading, Southampton, and Bournemouth; regional services to destinations in Northern England including Liverpool, Leeds, Sheffield, Newcastle and York; and local commuter services around Greater Manchester. It is one of 19 major stations managed by Network Rail. The station has 14 platforms, twelve terminal and two through platforms. Piccadilly is also a major interchange with the Metrolink light rail system with two tram platforms in its undercroft.', 'Title': 'Store Street (modern-day Manchester Piccadilly station) is opened by the Manchester and Birmingham Railway', 'Media': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Piccadilly_Station_Manchester_-_geograph.org.uk_-_692981.jpg/530px-Piccadilly_Station_Manchester_-_geograph.org.uk_-_692981.jpg', 'Source URL': 'https://en.wikipedia.org/wiki/Manchester_Piccadilly_station', 'Tag': 'Transport', 'Place': 'Manchester', 'Location': '53.477477, -2.230897', 'Date': '10/05/1842'}, {'Description': "HM Prison Manchester is a high-security men's prison in Manchester, England, operated by Her Majesty's Prison Service. It is still commonly referred to as Strangeways, which was its former official name derived from the area in which it is located, until it was rebuilt following a major riot in 1990.", 'Title': 'Strangeways Prison opens. First execution 29 March 1869', 'Media': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Strangeways-geograph-4634562-by-Peter-McDermott.jpg/440px-Strangeways-geograph-4634562-by-Peter-McDermott.jpg', 'Source URL': 'https://en.wikipedia.org/wiki/HM_Prison_Manchester', 'Tag': 'Conflict', 'Place': 'Manchester', 'Location': '53.492096, -2.246145', 'Date': '25/06/1868'}, {'Description': "Manchester Cenotaph is a war memorial in St Peter's Square, Manchester, England. Manchester was late in commissioning a First World War memorial compared with most British towns and cities; the city council did not convene a war memorial committee until 1922. The committee quickly achieved its target of raising \xc2\xa310,000 but finding a suitable location for the monument proved controversial. The preferred site in Albert Square would have required the removal and relocation of other statues and monuments, and was opposed by the city's artistic bodies. The next choice was Piccadilly Gardens, an area already identified for a possible art gallery and library; but in the interests of speedier delivery, the memorial committee settled on St Peter's Square. The area within the square had been had been purchased by the City Council in 1906, having been the site of the former St Peter's Church; whose sealed burial crypts remained with burials untouched and marked above ground by a memorial stone cross. Negotiations to remove these stalled so the construction of the cenotaph proceeded with the cross and burials in situ.", 'Title': ' Manchester Cenotaph, designed by Sir Edwin Lutyens, is unveiled', 'Media': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/MC-View_from_Town_Hall-3.jpg/440px-MC-View_from_Town_Hall-3.jpg', 'Source URL': 'https://en.wikipedia.org/wiki/Manchester_Cenotaph', 'Tag': 'Conflict', 'Place': 'Manchester', 'Location': '53.478867, -2.243015', 'Date': '12/07/1924'}, {'Description': 'Oasis were an English rock band formed in Manchester in 1991. Developed from an earlier group, the Rain, the band originally consisted of Liam Gallagher (lead vocals, tambourine), Paul "Bonehead" Arthurs (guitar), Paul "Guigsy" McGuigan (bass guitar) and Tony McCarroll (drums). Upon returning to Manchester, Liam\'s older brother, Noel Gallagher (lead guitar, vocals) joined as a fifth member, which formed the band\'s core and settled line-up. During the course of their existence, they had various line-up changes, though the Gallagher brothers remained as the staple members until the group\'s demise.', 'Title': 'Rock band Oasis play their first gig, at the Boardwalk club', 'Media': 'https://upload.wikimedia.org/wikipedia/commons/7/73/Oasis_Liam_and_Noel.jpg', 'Source URL': 'https://en.wikipedia.org/wiki/Oasis_(band)', 'Tag': 'Art', 'Place': 'Manchester', 'Location': '53.476946, -2.239224', 'Date': '18/08/1991'}, {'Description': 'The Liverpool and Manchester Railway (L&MR) was the first inter-city railway in the world. It opened on 15 September 1830 between the Lancashire towns of Liverpool and Manchester in England. It was also the first railway to rely exclusively on locomotives driven by steam power, with no horse-drawn traffic permitted at any time; the first to be entirely double track throughout its length; the first to have a signalling system; the first to be fully timetabled; and the first to carry mail.', 'Title': "The world's first purpose built passenger railway operated by steam locomotives", 'Media': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/First_passenger_railway_1830.jpg/440px-First_passenger_railway_1830.jpg', 'Source URL': 'https://en.wikipedia.org/wiki/Liverpool_and_Manchester_Railway', 'Tag': 'Transport', 'Place': 'Manchester', 'Location': '53.474176, -2.251060', 'Date': '15/09/1830'}, {'Description': 'Southern Cemetery is a large municipal cemetery in Chorlton-cum-Hardy, Manchester, England, 3 miles (4.8 km) south of the city centre. It opened in 1879 and is owned and administered by Manchester City Council. It is the largest municipal cemetery in the United Kingdom and the second largest in Europe.', 'Title': 'Southern Cemetery opens in Withington', 'Media': 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Southern_Cemetery%2C_Manchester_-_geograph.org.uk_-_1200101.jpg', 'Source URL': 'https://en.wikipedia.org/wiki/Southern_Cemetery,_Manchester', 'Tag': 'Construction', 'Place': 'Withington', 'Location': '53.430084, -2.261961', 'Date': '09/10/1879'}, {'Description': 'Sir Alexander Chapman Ferguson CBE (born 31 December 1941) is a Scottish former football manager and player who managed Manchester United from 1986 to 2013. He is considered one of the greatest managers of all time and he has won more trophies than any other manager in the history of football.', 'Title': 'Alex Ferguson takes over as manager of Manchester United F.C', 'Media': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Alex_Ferguson.jpg/440px-Alex_Ferguson.jpg', 'Source URL': 'https://en.wikipedia.org/wiki/Alex_Ferguson', 'Tag': 'Sport', 'Place': 'Manchester', 'Location': '53.458153, -2.272954', 'Date': '06/11/1986'}, {'Description': "Coronation Street (often referred to as Corrie) is a British soap opera created by Granada Television and shown on ITV since 9 December 1960. The programme centres on Coronation Street in Weatherfield, a fictional town based on inner-city Salford. In the show's fictional history, the street was built in 1902 and named in honour of the coronation of King Edward VII.", 'Title': 'The first episode of soap opera Coronation Street', 'Media': 'https://upload.wikimedia.org/wikipedia/en/8/86/Coronation_Street_Titles.png', 'Source URL': 'https://en.wikipedia.org/wiki/Coronation_Street', 'Tag': 'Art', 'Place': 'Manchester', 'Location': '53.478984, -2.254696', 'Date': '09/12/1960'}])
        os.system("rm -r holidays/event.dat")

    @ignore_warnings
    def testHoliday(self):
        """
           Tests that the holiday file is created
        """
        events = creatorGUI.readCSV("Events/TestRead.csv", "random", "all")
        self.assertTrue(os.path.exists("holidays/event.dat"))
        os.system("rm -r holidays/event.dat")


class TestDownloadImage(unittest.TestCase):
    @ignore_warnings
    def testFileCreated(self):
        """
           tests that an image file is created given the url link
        """
        creatorGUI.downloadImage(7357, "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/B_of_the_Bang_%28landscape%29.jpg/500px-B_of_the_Bang_%28landscape%29.jpg")
        self.assertTrue(os.path.exists("Events/Event7357.jpg"))
        os.system("rm -r Events/Event7357.jpg")

    @ignore_warnings
    def testWrongURL(self):
        """
           Test a file isnt created when a fake url is given
        """
        with self.assertRaises(requests.exceptions.MissingSchema) as cm:
            creatorGUI.downloadImage(7357, "Fake")
        self.assertFalse(os.path.exists("Events/Event7357.jpg"))

class TestCreateQR(unittest.TestCase):
    @ignore_warnings
    def testFileCreated(self):
        """
           tests that a file is created given the url
        """
        creatorGUI.createQR(7357, "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/B_of_the_Bang_%28landscape%29.jpg/500px-B_of_the_Bang_%28landscape%29.jpg")
        self.assertTrue(os.path.exists("Events/qr7357.png"))
        os.system("rm -r Events/qr7357.png")

class TestCreateTop(unittest.TestCase):
    @ignore_warnings
    def setUp(self):
        """
           Set up for the Tests
        """
        os.system("rm -r Resources/resized1.png")
        os.system("rm -r Resources/outPhoto1.jpg Resources/outputtext1-0.jpg")
        os.system("rm -r Resources/outputtext1-1.jpg Resources/outputWithText1.jpg")
        creatorGUI.createTop(1, "Events/Event1.jpg", "Events/Event1.txt", "Events/qr1.png",
        "test", "Resources/background2.png", "Helvetica")

    @ignore_warnings
    def testResize(self):
        """
           Test that the resized photo has been created
        """
        self.assertTrue(os.path.exists("Resources/resized1.png"))

    @ignore_warnings
    def testResizedSize(self):
        """
           Test that the size of the image is correct
        """
        image = Image.open("Resources/resized1.png")
        width, height = image.size
        self.assertLessEqual(width, 940)

    def testResizedSizeHeight(self):
        """
           Test that the size of the image is correct
        """
        image = Image.open("Resources/resized1.png")
        width, height = image.size
        self.assertLessEqual(height, 1000)


    @ignore_warnings
    def testImageWithBackground(self):
        """
           Tests the image of background and image is made
        """
        self.assertTrue(os.path.exists("Resources/outPhoto1.jpg"))

    @ignore_warnings
    def testOutputText(self):
        """
           tests output text file is created
        """
        self.assertTrue(os.path.exists("Resources/outputtext1-0.jpg"))

    @ignore_warnings
    def testOutputText2(self):
        """
           tests output text 2 file is created
        """
        self.assertTrue(os.path.exists("Resources/outputtext1-1.jpg"))

    @ignore_warnings
    def testOutputWithText(self):
        """
           tests output text with file is created
        """
        self.assertTrue(os.path.exists("Resources/outputWithText1.jpg"))

class TestCreatePDF(unittest.TestCase):
    @ignore_warnings
    def setUp(self):
        """
           Call create PDF to set up the Tests
        """
        creatorGUI.createPDF("TestCases")

    @ignore_warnings
    def testNoTiff(self):
        """
           Test that the Tiff file is deleted
        """
        self.assertFalse(os.path.exists("HistoryCalendar/Calendar.tiff"))
        os.system("rm -r TestCases.pdf")

    @ignore_warnings
    def testFileCreated(self):
        """
           Test that the pdf of that name has been created
        """
        self.assertTrue(os.path.exists("TestCases.pdf"))
        os.system("rm -r TestCases.pdf")

class TestCreateCal(unittest.TestCase):
    @ignore_warnings
    def setUp(self):
        """
           Set up for the calendar to be created
        """
        os.system("rm -r HistoryCalendar/Calendar01.jpg HistoryCalendar/HistoryCalendar1.jpg")
        monthInfo = creatorGUI.readCSV("Events/events.csv", "random", "all")
        creatorGUI.createCal(1, monthInfo, "Resources/background.jpg", "TESTING", "TESTING", "Resources/background2.png", "Helvetica")

    @ignore_warnings
    def testCalendarDates(self):
        """
           Test that the dates file has been created
        """
        self.assertTrue(os.path.exists("HistoryCalendar/HistoryCalendar1.jpg"))
        os.system("rm -r holidays/event.dat")

    @ignore_warnings
    def testCalendarFull(self):
        """
           Test that the calendar image has been created
        """
        self.assertTrue(os.path.exists("HistoryCalendar/Calendar01.jpg"))
        os.system("rm -r holidays/event.dat")

if __name__ =='__main__':
    unittest.main()
