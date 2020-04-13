import unittest
import selector
import os
import warnings

def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test

class TestGetParser(unittest.TestCase):
    @ignore_warnings
    def testParserCreated(self):
        """
           Test that a parser is created and returned
        """
        parser = selector.get_parser()
        self.assertTrue(parser)

class TestTitleChoices(unittest.TestCase):
    @ignore_warnings
    def testGetsTitles(self):
        """
           Tests that a list is returned and is not empty
        """
        os.system("cp Events/events.csv current.csv")
        rows = selector.title_choices(1)
        self.assertTrue(rows)
        
    @ignore_warnings
    def testTitlesJanuary(self):
        """
           Test the correct titles for january are created
        """
        os.system("cp Events/events.csv current.csv")
        rows = selector.title_choices(1)
        self.assertEquals(rows, ['Britain\'s tallest self-supporting sculpture, the "B of the Bang", is unveiled in Manchester',
        'The Avro Manchester Mark III BT308, prototype of the Avro Lancaster heavy bomber, first flies, from RAF Ringway',
        'Telephony in Greater Manchester: first such telephone in regular use in the country',
        ' Manchester Victoria station is opened by the Manchester and Leeds Railway',
        ' The Hallé gives its first concert as a permanent orchestra',
        'John Rylands Library', 'Sunny Lowry - first British woman to swim the English Channel is born',
        'Astromoners Andrew Lyne, Michael Kramer, and collaborators at Jodrell Bank discovered the double pulsar ',
        "Ashburne House, Victoria Park, Manchester University's first Hall of Residence for women opens",
        'Edward Schunk dies leaving his Laboratory and library to the Victoria University'])

    @ignore_warnings
    def testTitlesJune(self):
        """
           Test the correct titles for June are created
        """
        os.system("cp Events/events.csv current.csv")
        rows = selector.title_choices(6)
        self.assertEquals(rows, ['Alan Turing commits suicide ',
        'Manchester Aquatics Centre opens for the Commonwealth Games',
        'The corner stone of the new Mechanics Building on Princess street is laid by Mr Oliver Heywood',
        'The Christie Building is opened',
        "St Ann's Church, sponsored by Ann, Lady Bland, is consecrated",
        'The first Theatre Royal opens in Spring Gardens',
        "Inaugural meeting of the national Trades Union Congress held at the Mechanics' Institute",
        'Strangeways Prison opens. First execution 29 March 1869',
        'Manchester Airport at Ringway opens',
        "World's first working program run on an electronic stored-program computer, the Manchester Baby",
        '1996 Manchester bombing'])

if __name__ =='__main__':
    unittest.main()
