"""
I am getting the existing results from a CSV, scrape new results, compare which new results
are actually new (don't exist in results) and write the whole (updated) collection of results to the CSV

After scraping, I run processing.py to add points to results and riders.
Then I add up all points for all the teamcaptains.

"""
import requests
from bs4 import BeautifulSoup
import process_files, count_riders, change_category, first_cycling, add_dates
from datetime import datetime
# from operator import itemgetter


results = process_files.read_csv_file('all_results.csv')

# write a line to processed.txt to indicate when the results were checked
# this also makes sure the process runs without error, even if there are no new results
# by writing a line to processed.txt, there is a change in files, so the site build works
now =  datetime.now()
file1 = open("processed.txt", "a")  # append mode
file1.write(f"Resultaten gecheckt: { now } \n")
file1.close()


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

    WIP: there is a (prov.) after the racename, to indicate provisional results.
    Store these and re-visit, until (prov.) or (provisional) disclaimer is gone.
    """
    print("OK, checking new results")
    base_result_url = "https://cqranking.com/men/asp/gen/start.asp"
    b = base_result_url
    r = requests.get(b)
    soup = BeautifulSoup(r.text, "html.parser")
    result_table =  soup.find("table", ["borderNoOpac"])
    row_tags = result_table.find_all('tr')[1:] # skipping the header rows
    for row_tag in row_tags:
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
        date = tds[0].text
        if len(date) < 8:
            # WIP: year hardcoded, use VARIABLE
            parts = date.split("/")
            date = date + "/2023"
        rank = tds[4].text.split(".")[0]
        category = tds[1].text
        race_name = tds[3].text
        if not category[:3] in ['1.2','2.2']:
            country = tds[2].find('img').get('title').upper()
            
            race_id = tds[3].a['href'].split("=")[1]
            rider = tds[4].text.split(".")[1]
            rider_id = tds[4].a['href'].split("=")[1]

            if (category[-1] == 's' or category[-1] == 'r' or category[:3] == 'NCT' or category[:3] == 'CCT') and (category[:3] not in ['1.2','2.2']):
                # print("add race to new results")
                if category=='2.WT2s':
                    category = change_category.new_category(race_name, category)
                if category[:3] == 'NCT':
                    category = count_riders.change_category_NCTT(country)
                    print(f"New category for {race_name}, changed to {category}")
                new_results.append([int(rank), category, race_name, int(race_id), rider.strip(), int(rider_id), float(points), int(JPP), date])
                # this is where we get the results for jersey wearers in GT from first_cycling
                if category in ['GT1s', 'GT2s']:
                    get_jersey_ranking(race_name, race_id, category, date)
            else:
                if category[:4]=='1.WT' or category[:4]=='2.WT':
                    category = change_category.new_category(race_name, category)
                get_results_per_race(race_id, race_name, category, country)



def get_jersey_ranking(race_name, race_id, category, date):
    points = 0
    JPP = 0
    # WIP: get the year from date. Now using default year in first_cycling.scrape_result
    rider_id, rider = first_cycling.scrape_result(race_name, 'gc')
    if rider_id:
        new_results.append([0, category, "Leiderstrui na " + race_name, int(race_id), rider.strip(), int(rider_id), float(points), int(JPP), date])
    rider_id, rider = first_cycling.scrape_result(race_name, 'youth')
    if rider_id:
        new_results.append([-1, category, "Jongerentrui na " + race_name, int(race_id), rider.strip(), int(rider_id), float(points), int(JPP), date])
    rider_id, rider = first_cycling.scrape_result(race_name, 'point')
    if rider_id:
        new_results.append([-2, category, "Puntentrui na " + race_name, int(race_id), rider.strip(), int(rider_id), float(points), int(JPP), date])
    rider_id, rider = first_cycling.scrape_result(race_name, 'mountain')
    if rider_id:
        new_results.append([-3, category, "Bergtrui na " + race_name, int(race_id), rider.strip(), int(rider_id), float(points), int(JPP), date])

# get_jersey_ranking('Tour de France, Stage 1 : Budapest - Visegrad (195 km)', 39757, 'GT1s', '06/05/2022')

# def test_old_GT_stages(starturl):
#     """
#     starturl is the page  with all the stages from a GT (Tour, Giro, Vuelta)
#     For instance, https://cqranking.com/men/asp/gen/tour.asp?tourid=4203

#     From this page I want to get the info to feed into get_jersey_rankings, like:
#     - race_name, 
#     - race_id,
#     - category,
#     - date
#     """
#     r = requests.get(starturl)
#     soup = BeautifulSoup(r.text, "html.parser")
#     tables =  soup.find_all("table")
#     result_table = tables[10]
#     row_tags = result_table.find_all('tr')[1:] # skipping the header rows
#     for row_tag in row_tags:
#         tds = row_tag.find_all('td')
#         """
#         1 - date (Not using this yet.. I should!)
#         1 - category
#         2 - country
#         3 - Name race + href full results
#         4 - rank + name rider + href rider
#         """
#         date = tds[1].text
#         date = str(date) + "/2022"
#         race_id = tds[7].a['href'].split("=")[1]
#         race_name = tds[7].text
#         country = tds[3].find('img').get('title').upper()
#         races = {'ITA': ['Giro d\'Italia', 'GT2s'], 'FRA': ['Tour de France', 'GT1s'], 'ESP': ['Vuelta a España', 'GT2s']}
#         category = races[country][1]
#         print(race_name, race_id, category, date)
#         if race_name[:5] == "Stage":
#             race_name = races[country][0] = " " + race_name
#             get_jersey_ranking(race_name, race_id, category, date)


# test_old_GT_stages("https://cqranking.com/men/asp/gen/tour.asp?tourid=4203")

def get_results_per_race(race_id, race_name, category, country=None):
    """
    WIP:
    Break this up in two functions. 
    First is "number_of_rankings" which returns the number of rankings to be scraped.
    Second is the scraping part of this function, can have the same name, add
    rankings to the function call.
    """
    if category not in ['1.2','2.2']:
        if category[-1] == "s" or category[-1] == "r":
            # stage, mountains/points only get winner (and sometimes also leader)
            rankings = 1 
        elif category in ['1.1', '2.1']:
            # only get top 3
            rankings = 3
        elif category == 'GT1':
            # Tour de France, get top 20
            rankings = 20
        elif category == 'GT2':
            # grandtour, get top 15 (Giro, Vuelta)
            rankings = 15
        elif category[:3] == 'NCT':
            # count riders of country being sold
            rankings = count_riders.get_timetrial(country)
        elif category[:2] == 'NC':
            # count riders of country being sold
            rankings = count_riders.get_roadrace(country)
        else:
            # all others have top 10 for JPP
            rankings = 10
        
        base_result_url = "https://cqranking.com/men/asp/gen/race.asp?raceid="
        b = base_result_url + str(race_id)
        r = requests.get(b)
        soup = BeautifulSoup(r.text, "html.parser")
        result_table =  soup.find("table", ["borderNoOpac"])
        #print(result_table)
        date = result_table.find("td", ["textwhite"]).text
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
                # replace category for NC and NCT races
                if category[:3] == 'NCT':
                    category = count_riders.change_category_NCTT(country)
                elif category[:2] == 'NC':
                    category = count_riders.change_category_NCRR(country)
                new_results.append([int(rank), category, race_name, int(race_id), rider.strip(), int(rider_id), float(points), int(JPP), date])
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


full_results.insert(0,['rank','category','racename','race_id','rider_name','rider_id','points','jpp','date'])

# Now store the results in a CSV file
process_files.write_csv_file('all_results.csv', full_results)
# and store the new_results is another CSV file
# add header row first
new_results.insert(0,['rank','category','racename','race_id','rider_name','rider_id','points','jpp','date'])
process_files.write_csv_file('latest_results.csv', new_results)


# with open('_data/all_results.csv', 'w') as f:
#     write = csv.writer(f)
#     write.writerows(full_results)

# with open('_CSV/updated_results.csv', 'w') as f:
#     write = csv.writer(f)
#     write.writerows(unique_results)
