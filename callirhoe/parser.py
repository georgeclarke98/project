import csv
import random
import gspread
import pandas
import os
import sys
import lib
from oauth2client.service_account import ServiceAccountCredentials

def parseOwn():
    #interact with the google docs api using own credentials
    print("Authorizing access to spreadsheet")
    scope = ["https://spreadsheets.google.com/feeds"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
    client = gspread.authorize(credentials)

    #open the wanted sheet
    print("Opening spreadsheet")
    manchesterCorpus = client.open_by_key('1BNti0T_yNtpwsparOIbHb21nthnVfNVPe4ZGUAQTB6o').sheet1

    #convert spreadsheet to a csv file
    print("Creating CSV file from spreadsheet")
    filename = "Events/events.csv"
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(manchesterCorpus.get_all_values())

def parseUsersExcel(location, name):
    file = pandas.read_excel(location)
    print("Creating CSV file from spreadsheet")
    file.to_csv("Events/" + name + ".csv", index=None, header=True)
    #save the file as a csv to be used in the creator application
    print("Your csv file has been saved in Events/" + name + ".csv")

def main_program():
    choice = input("Do you have a corpus to use? (y/n): ")
    #ask if the user wants to use own corpus
    while(choice != "n" and choice != "y"):
        choice = input("Please answer 'y' or 'no': ")
    if choice == "n":
        print("Using Manchester corpus!")
        parseOwn()
        #if the user has no corpus just use the current one
    elif choice == "y":
        print("Reminder: Corpus must be in the form of an excel spreadsheet with the correct formatting!")
        location = input("Please enter the location the corpus:")
        #get the user to enter the url for their corpus
        name = input("Please choose a name for  your csv file: ")
        parseUsersExcel(location, name)
        #parse the own users excel spreadsheet

if __name__ == "__main__":
    try:
        main_program()
    except lib.Abort as e:
        sys.exit(e.args[0])
