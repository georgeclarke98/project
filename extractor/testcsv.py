import sqlite3
import pandas
def SqltoCsv():
    con = sqlite3.connect('/Users/jay/Desktop/extra_sqlite/history.db')
    table = pandas.read_sql('select * from calendar_info', con)
    table.to_csv('/Users/jay/Desktop/extra_sqlite/output.csv')

SqltoCsv()
