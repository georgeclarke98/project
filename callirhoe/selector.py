import lib
import csv
import pandas
from gooey import Gooey, GooeyParser

def title_choices(month):
    reader = csv.DictReader(open("current.csv"))
    rows = [row["Title"] for row in reader if "/%02d/" % month in row["Date"] and row["Media"] != ""]
    return rows

def get_parser():
    """
        Get the argument parser for requirements
    """

    parser = GooeyParser(description="Event selector for the calendar creator")
    #create the parser
    parser.add_argument("January", widget='Dropdown',
                        choices=title_choices(1),
                        help="Choose the event for January")
    parser.add_argument("February", widget='Dropdown',
                        choices=title_choices(2),
                        help="Choose the event for February")
    parser.add_argument("March", widget='Dropdown',
                        choices=title_choices(3),
                        help="Choose the event for March")
    parser.add_argument("April", widget='Dropdown',
                        choices=title_choices(4),
                        help="Choose the event for April")
    parser.add_argument("May", widget='Dropdown',
                        choices=title_choices(5),
                        help="Choose the event for May")
    parser.add_argument("June", widget='Dropdown',
                        choices=title_choices(6),
                        help="Choose the event for June")
    parser.add_argument("July", widget='Dropdown',
                        choices=title_choices(7),
                        help="Choose the event for July")
    parser.add_argument("August", widget='Dropdown',
                        choices=title_choices(8),
                        help="Choose the event for August")
    parser.add_argument("September", widget='Dropdown',
                        choices=title_choices(9),
                        help="Choose the event for September")
    parser.add_argument("October", widget='Dropdown',
                        choices=title_choices(10),
                        help="Choose the event for October")
    parser.add_argument("November", widget='Dropdown',
                        choices=title_choices(11),
                        help="Choose the event for November")
    parser.add_argument("December", widget='Dropdown',
                        choices=title_choices(12),
                        help="Choose the event for December")
    return parser

@Gooey(required_cols=1)
def main_program():
    parser = get_parser()
    args = parser.parse_args()
    #parse the arguments to get the choices

    reader = csv.DictReader(open("current.csv"))
    writer = csv.DictWriter(open("eventsSelected.csv", "w"), fieldnames=reader.fieldnames, extrasaction='ignore')
    writer.writeheader()
    #create the writer and write the headfings 
    for month in range(1,13):
        reader = csv.DictReader(open("current.csv"))
        rows = [row for row in reader]

        if month == 1:
            current = ([row for row in rows if args.January in row["Title"]])
            writer.writerow(current[0])
        elif month == 2:
            current = ([row for row in rows if args.February in row["Title"]])
            writer.writerow(current[0])
        elif month == 3:
            current = ([row for row in rows if args.March in row["Title"]])
            writer.writerow(current[0])
        elif month == 4:
            current = ([row for row in rows if args.April in row["Title"]])
            writer.writerow(current[0])
        elif month == 5:
            current = ([row for row in rows if args.May in row["Title"]])
            writer.writerow(current[0])
        elif month == 6:
            current = ([row for row in rows if args.June in row["Title"]])
            writer.writerow(current[0])
        elif month == 7:
            current = ([row for row in rows if args.July in row["Title"]])
            writer.writerow(current[0])
        elif month == 8:
            current = ([row for row in rows if args.August in row["Title"]])
            writer.writerow(current[0])
        elif month == 9:
            current = ([row for row in rows if args.September in row["Title"]])
            writer.writerow(current[0])
        elif month == 10:
            current = ([row for row in rows if args.October in row["Title"]])
            writer.writerow(current[0])
        elif month == 11:
            current = ([row for row in rows if args.November in row["Title"]])
            writer.writerow(current[0])
        elif month == 12:
            current = ([row for row in rows if args.December in row["Title"]])
            writer.writerow(current[0])
        else:
            print("Month out of range ")
        #add the event for each month to the events list
    print("\n\n\n\n\nPlease Close This Window!")

if __name__ == "__main__":
    try:
        main_program()
    except lib.Abort as e:
        sys.exit(e.args[0])
