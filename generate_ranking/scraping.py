"""
I am getting the existing results from a CSV, scrape new results, compare which new results
are actually new (don't exist in results) and write the whole (updated) collection of results to the CSV

Update:
I am struggling to remove doubles, so why not add the lists together and make a set out of it?
"""
import requests
from bs4 import BeautifulSoup
import process_files
from datetime import datetime
# from operator import itemgetter


results = process_files.read_csv_file('all_results.csv')

# backup the existing results, use datetime
today =  datetime.today()
print(today)
filename = 'backup/'+str(today)+".csv"
print(filename)
process_files.write_csv_file(filename, results)

new_results = []

                # [['rank',
                # 'category',
                # 'race_name',
                # 'race_id',
                # 'rider',
                # 'rider_id',
                # 'points',
                # 'JPP']]

def check_if_new_results():
    """
    We don't want the scraper to run if there are no new results. 
    We visit CQranking, check teh latest result(s). 
    If we already have that result, we cancel.
    Otherwise, we scrape.
    We could/(should?) run the normal scraper once a day regardless?
    """
    # base_result_url = "https://cqranking.com/men/asp/gen/start.asp"
    # b = base_result_url
    # r = requests.get(b)
    # soup = BeautifulSoup(r.text, "html.parser")
    # result_table =  soup.find("table", ["borderNoOpac"])
    # row_tags = result_table.find_all('tr')[1:2] # just first result, skipping header row
    # for row_tag in row_tags:
    #     try:
    #         tds = row_tag.find_all('td')
    #         """
    #         0 - date (Not using this yet.. I should!)
    #         1 - category
    #         2 - country
    #         3 - Name race + href full results
    #         4 - rank + name rider + href rider
    #         """
    #         rank = tds[4].text.split(".")[0]
    #         race_id = tds[3].a['href'].split("=")[1]
    #         print(f"Check resultaat, {tds[3].text}")
    #         for result in results:
    #             if (int(rank) == int(result[0]) and int(race_id) == int(result[3])):
    #                 print(f"{race_id} already exists with rank {rank}")
    #         return True
    #     except:
    #         print("Something went wrong scraping latest results")
    #         return False
    return True



def get_results():
    """
    Check https://cqranking.com/men/asp/gen/start.asp to see if there are new results.
    Open CSV with already scraped results and compare. That means two lists, compare new results (shorter list)
    with existing results
    If there are results missing, get them by running get_results_per_race.

    WIP: there is a (prov.) aftre the racename, to indicate provisional results.
    Store these and re-visit, until (prov.) or (provisional) disclaimer is gone.
    """
    if check_if_new_results():
        print("OK, checking new results")
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
                0 - date (Not using this yet.. I should!)
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
                if not category[:3] in ['1.2','2.2']:
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
                # else:
                #     #print("skip this category")
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

"""
Undoubling results is a bitch.
I am creating a list of race_id and rank to keep track of the results I already scraped.

New list, add race_id and rank to it, check if we already have that result, if not,
add it to both lists.
"""
race_rank_results = []
full_results = []
for nr in new_results:
    if [int(nr[0]),int(nr[3])] not in race_rank_results:
        race_rank_results.append([int(nr[0]),int(nr[3])])
        full_results.append(nr)

for r in results[1:]:
    # results has a header row, which we skip and at the end add it again
    if [int(r[0]),int(r[3])] not in race_rank_results:
        race_rank_results.append([int(r[0]),int(r[3])])
        full_results.append(r)


full_results.insert(0,['rank','category','racename','race_id','rider_name','rider_id','points','jpp'])

# Now store the rsults in a CSV file
process_files.write_csv_file('all_results.csv', full_results)
# and store the new_results is another CSV file
# add header row first
new_results.insert(0,['rank','category','racename','race_id','rider_name','rider_id','points','jpp'])
process_files.write_csv_file('latest_results.csv', new_results)


# with open('_data/all_results.csv', 'w') as f:
#     write = csv.writer(f)
#     write.writerows(full_results)

# with open('_CSV/updated_results.csv', 'w') as f:
#     write = csv.writer(f)
#     write.writerows(unique_results)
