import unittest
import parser
import os
import warnings
import csv
import xlrd

def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test

class TestParseOwn(unittest.TestCase):
    @ignore_warnings
    def test_file_exists(self):
        """
           Tests that a file has been created
        """
        os.system("rm -r Events/events.csv")
        parser.parseOwn()
        #Remove the current events file and
        self.assertTrue(os.path.exists("Events/events.csv"))

    @ignore_warnings
    def test_contents(self):
        """
           Tests that the contents in the created file is correct
        """
        reader = csv.DictReader(open("Events/events.csv"))
        self.assertEquals(reader.fieldnames,
        ['Title','Date','Description','Place','Location','Media','Source URL','Tag'])

class TestParseUsers(unittest.TestCase):
    @ignore_warnings
    def test_file_exists(self):
        """
           Tests that a file has been created from excel
        """
        parser.parseUsersExcel("tests/test.xlsx", "test")
        self.assertTrue(os.path.exists("tests/test.csv"))

    @ignore_warnings
    def test_contents(self):
        """
           Tests that the contents in the created file is correct
        """
        reader = csv.DictReader(open("tests/test.csv"))
        rows = [row for row in reader]
        self.assertEquals(reader.fieldnames,['Title', 'Date'])
        self.assertEquals(rows, [{'Title': 'Britain\'s tallest self-supporting sculpture, the "B of the Bang", is unveiled in Manchester', 'Date': '2005-01-12 00:00:00'},
        {'Title': 'The Avro Manchester Mark III BT308, prototype of the Avro Lancaster heavy bomber, first flies, from RAF Ringway', 'Date': '1941-01-09 00:00:00'},
        {'Title': 'Telephony in Greater Manchester: first such telephone in regular use in the country', 'Date': '26/01/1878'},
        {'Title': ' Manchester Victoria station is opened by the Manchester and Leeds Railway', 'Date': '01/01/1844'},
        {'Title': ' The Hallé gives its first concert as a permanent orchestra', 'Date': '30/01/1858'}])

    @ignore_warnings
    def testWrongFileType(self):
        """
           tests that an error is thrown when a .txt file is given
        """
        with self.assertRaises(xlrd.XLRDError) as cm:
            parser.parseUsersExcel("tests/test.txt", "test")


if __name__ =='__main__':
    unittest.main()
