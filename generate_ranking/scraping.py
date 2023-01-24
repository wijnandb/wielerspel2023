"""
I am getting the existing results from a CSV, scrape new results, compare which new results
are actually new (don't exist in results) and write the whole (updated) collection of results to the CSV

Update:
I am struggling to remove doubles, so why not add the lists together and make a set out of it?
"""
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

with open('CSV/all_results.csv', newline='') as f:
    readresults = csv.reader(f)
    if not readresults:
        results = []
    else: 
        results = list(readresults)
    

new_results = []

                # [['rank',
                # 'category',
                # 'race_name',
                # 'race_id',
                # 'rider',
                # 'rider_id',
                # 'points',
                # 'JPP']]


def get_results():
    """
    Check https://cqranking.com/men/asp/gen/start.asp to see if there are new results.
    Open CSV with already scraped results and compare. That means two lists, compare new results (shorter list)
    with existing results
    If there are results missing, get them by running get_results_per_race.

    WIP: there is a (prov.) aftre the racename, to indicate provisional results.
    Store these and re-visit, until (prov.) or (provisional) disclaimer is gone.
    """

    base_result_url = "https://cqranking.com/men/asp/gen/start.asp"
    b = base_result_url
    r = requests.get(b)
    soup = BeautifulSoup(r.text, "html.parser")
    result_table =  soup.find("table", ["borderNoOpac"])
    row_tags = result_table.find_all('tr')[1:] # skipping the header rows
    for row_tag in row_tags:
        try:
            tds = row_tag.find_all('td')
            """
            0 - date
            1 - category
            2 - country
            3 - Name race + href full results
            4 - rank + name rider + href rider
            """
            points = 0
            JPP = 0
            rank = tds[4].text.split(".")[0]
            category = tds[1].text
            #print(category)
            if category[:3] in ['1.2','2.2']:
                print("skip this category")
            else:
                #country = tds[2].text
                race_name = tds[3].text
                race_id = tds[3].a['href'].split("=")[1]
                rider = tds[4].text.split(".")[1]
                rider_id = tds[4].a['href'].split("=")[1]

                if (category[-1] == 's' or category[-1] == 'r' or category[:2] == 'NC') and (category[:3] not in ['1.2','2.2']):
                    #print("add race to new results")
                    new_results.append([int(rank), category, race_name, int(race_id), rider.strip(), int(rider_id), float(points), int(JPP)])
                else:
                    get_results_per_race(race_id, race_name, category)
        except:
            print("Something went wrong scraping latest results")


def get_results_per_race(race_id, race_name, category):
    """
    WIP:
    Appending results can lead to double results.
    Writing results means getting all results every day again, which is unnecessary
    (and is causing another problem, where I only have the rsults of the last race...)
    """
    if category not in ['1.2',['2.2']]:
        if category[-1] == "s" or category[-1] == "r" or category in ['NC2','NC3','NC4','NC5'] or category[:3] == 'NCT':
            # stage, mountains/points, national championships only get winner (and sometimes also leader)
            rankings = 2 
        elif category in ['1.1', '2.1']:
            # only get top 3
            rankings = 3
        elif category in ['GT1', 'GT2']:
            # grandtour, get top 15 or top 20
            rankings = 20
        else:
            # all others have top 10 for JPP (expec)
            rankings = 10
        
        base_result_url = "https://cqranking.com/men/asp/gen/race.asp?raceid="
        b = base_result_url + str(race_id)
        r = requests.get(b)
        soup = BeautifulSoup(r.text, "html.parser")
        first_result = soup.find("td", ["tabrow1", "tabrow2"])
        result_tr = first_result.parent
        result_table = result_tr.parent
    
        row_tags = result_table.find_all('tr')[1:rankings+1] # skipping the header row, top x only

        for row_tag in row_tags:
            points = 0
            JPP = 0
            try:
                tds = row_tag.find_all('td')
                if tds[1].text == 'leader':
                    rank = 0
                else:
                    rank = tds[1].text.split(".")[0]
                rider_id = tds[5].a['href'].split("=")[1]
                rider = tds[5].text
                new_results.append([int(rank), category, race_name, int(race_id), rider.strip(), int(rider_id), float(points), int(JPP)])
                #print("Added new result")
            except:
                continue

get_results()

def unique_items(L):
    found = set()
    for item in L:
        if item not in found:
            yield item
            found.add(item)

updated_results = results + new_results
unique_results = unique_items(updated_results)


with open('CSV/all_results.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(new_results)

with open('CSV/updated_results.csv', 'w') as f:
    write = csv.writer(f)
    write.writerows(unique_results)
