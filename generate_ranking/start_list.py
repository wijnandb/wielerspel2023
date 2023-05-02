"""
For each race a startlist is published on FirstCycling.
https://firstcycling.com/race.php?r=12&y=2023&k=start
r = race_id.
y = year 
and k = start means startlist

The idea is to go over this list, get all the riders and their (cqranking) id's and then
look up the team_captain.

We can then show a table with the riders and their team captains.

If we use datatables, we don't even have to think about sorting, searching etc.

On the page, we look for tables. The first table has nothing, the others each hold a ccyling team with riders.
"""
import requests
from bs4 import BeautifulSoup
import process_files, first_cycling, add_teamcaptains

riders = process_files.read_csv_file('all_riders_cqranking.csv')

# eventually we need to store it in a startlist csv
# but for now we just print it
startlist = [['race_id', 'start_number', 'rider', 'cq_rider_id', 'team', 'country', 'team_captain', 'team_captain_id', 'price']]


def get_riders(race_id, year='2023'):
    start_url = "https://firstcycling.com/race.php?r="+race_id+"&y="+year+"&k=start"
    print(start_url)

    r = requests.get(start_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    result_tables = soup.find_all('table')

    # the first table is empty, the others are the teams
    for table in result_tables[2:]:
        header = table.find('th')
        team = header.text
        body = table.find('tbody')
        rows = body.find_all('tr')
        for row in rows:
            tds = row.find_all('td')
            # print(tds)
            start_number = tds[0].text.strip()
            country = tds[1].find('img').get('title')
            rider = tds[1].find('a').get('title').strip()
            rider_id = first_cycling.ridername_to_id(rider, country)
            ploegleider, ploegleider_id, points = add_teamcaptains.add_teamcaptain_to_startlist(rider_id)
            # if ploegleider != '-':
            print(race_id, start_number, rider, rider_id, team, country, ploegleider, ploegleider_id)
            startlist.append([race_id, start_number, rider, rider_id, team, country, ploegleider, ploegleider_id, points]) 

    process_files.write_csv_file('startlist.csv', startlist)

get_riders('13', '2023')



