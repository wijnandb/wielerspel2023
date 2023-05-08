"""
- Open the csv file with the results
- open page on cqranking with race_id
- get the date
- add date to the results
- save csv file
"""
import process_files
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

results = process_files.read_csv_file('all_results.csv')
# updated_results = []
# results[0].append("datum")

def add_missing_date_to_results(file):
    results = process_files.read_csv_file(file)
    updated_results = []
    for result in results[1:]:
        if len(result) < 9:
            date = get_date_for_result(result[3])
            result.insert(8, date)
        elif not result[8]:
            date = get_date_for_result(result[3])
            result[8] = date
        updated_results.append(result)
    process_files.write_csv_file(file, updated_results)


def get_date_for_result(race_id):
    base_url = "https://cqranking.com/men/asp/gen/race.asp?raceid="
    b = base_url + str(race_id)
    r = requests.get(b)
    soup = BeautifulSoup(r.text, "html.parser")
    result_table =  soup.find("table", ["borderNoOpac"])
    date = result_table.find("td", ["textwhite"])
    print(date.text)
    date_object = convert_date(date.text)
    return date_object

# add_missing_date_to_results("all_results.csv")
# get_date_for_result(41261)

def convert_date(string):
    datetime_object = datetime.strptime(string, '%d/%m/%Y').date()
    return datetime_object

def convert_all_dates():
    for result in results[1:]:
        if len(result) < 9:
            pass
        else:
            date = convert_date(result[8])
            result[8] = date
    process_files.write_csv_file("all_results.csv", results)


# convert_all_dates()