import unittest2 as unittest
import warnings
import creatorGUI
import os
import requests

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

# class TestReadCSV(unittest.TestCase):
#     @ignore_warnings

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

class TestCreateQR(unittest.TestCase):
    @ignore_warnings
    def testFileCreated(self):
        """
           tests that a file is created given the url
        """
        creatorGUI.createQR(7357, "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/B_of_the_Bang_%28landscape%29.jpg/500px-B_of_the_Bang_%28landscape%29.jpg")
        self.assertTrue(os.path.exists("Events/qr7357.png"))
        os.system("rm -r Events/qr7357.png")


# class TestCreateTop(unittest.TestCase):
#     TODO
#
# class TestCreatePDF(unittest.TestCase):
#     TODO
#
# class TestCreateCal(unittest.TestCase):
#     TODO

if __name__ =='__main__':
    unittest.main()
