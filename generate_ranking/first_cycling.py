import requests
from bs4 import BeautifulSoup
import process_files

""""
Some results are not on CQranking, for innstance for the Big Tours
we also award points for the leaders of the GC, the points and mountains ranking 
and for the best young rider in the GC.

On First Cycling, we can find those results.
The url is https://firstcycling.com/race.php?r=13&y=2022&e=
r=13 is Giro d'Italia

y is the year and 
e is the stage number

Without a value for e, we get the final GC results.

There are different divs for each ranking:
div id="gc" is the General Classification
div id="youth" is the best young rider
div id="point" is the points ranking
div id="mountain" is the mountains ranking

Within the div there is a table with the results.
In the first tr is the leader.
td 0 contains the position
td 1 is hidden and contains the year of birth of the rider
td 2 has an image with the flag of country of the rider
td 3 has an href with rider_id (this is a different rider_id than the one on CQranking),
a span with the last name and the first name in text.
td 4 has an href with the team name
td 5 has UCI points
td 6 has the time

These functions get called from the 'normal' scraping process and return the cq_riderid



"""
riders = process_files.read_csv_file('all_riders_cqranking_with_fc_rider_id.csv')

def scrape_result(racename, jersey, year=2023):
    """
    Visit the page.
    Get the number 1 for the different rankings.
    Find the CQranking id for the rider
    Create a result line, containing:

    - rank
    - category
    - race_name
    - race_id ??
    - rider
    - rider_id (CQranking id)
    - points
    - JPP
    Or: call this function with a specific stage number, to get 
    - the stage winner (if at all necessary)
    - the leader jerseys

    There are different divs for each ranking:
        div id="sta" is the stage result
        div id="gc" is the General Classification
        div id="youth" is the best young rider
        div id="point" is the points ranking
        div id="mountain" is the mountains ranking
    
    """
    race_id = str(racename_to_id(racename))
    # print(f"{racename} omgezet naar id: {race_id}")
    stage = str(stagename_to_number(racename))
    year = str(year)
    base_result_url = "https://firstcycling.com/race.php?r="+race_id+"&y="+year+"&e="+stage
    # print(base_result_url)
    b = base_result_url
    r = requests.get(b)
    soup = BeautifulSoup(r.text, "html.parser")
    # get the different rankings
    div = soup.find("div", id=jersey)
    # print(div)
    if div:
        print(f"Looking for wearer of {jersey} jersey")
        table = div.find("tbody")
        tablerow = table.find("tr")
        # print(tablerows[:1])
        # for tablerow in tablerows[:1]:
        tds = tablerow.find_all("td")
        if len(tds) == 1:
            return "Nog geen uitslag bekend"
        # print(tds[0].text)
        if tds[0].text not in ['01','1']:
            print(f"Did not find a number 1, in race { race_id } for year { year}")
        else:
            name = tds[1].text.strip()
            print(f"Found {name} as wearer of {jersey} jersey")
            link = tds[3].find('a').get('href').split('=')[1]
            fc_rider_id = link.split('&')[0]
            print(f"Found rider_id {fc_rider_id} for {name}")
            # year_of_birth = tds[1].text.strip()
            # country = tds[2].find('img').get('title')
        
            """
            Now I want to get the rider_id from CQranking
            by passing in the rider name
            """
            rider_id = ridername_to_id(name, fc_rider_id)
            return rider_id, name
    else:
        return None


def ridername_to_id(name, fc_rider_id, country=0, year_of_birth=0):
    """
    I want to look up/find the CQrider_id 
    
    I have a list of all known active riders from CQRanking.
    The (interesting) fields are:
    - UCICode, which contains both three-letter nationality and year of birth, so that could be interesting to use
    - Full name, with last name(s) first and then first name(s)
    Let's start simple, just loop over the riders until I have a match, which means the
    full name from first cycling equals the full name at CQranking.
    """
    from unidecode import unidecode

    for rider in riders[1:]:
        if len(rider) > 9:
            if int(fc_rider_id) == int(rider[9]):
                # print(f"Match gevonden {name } op id voor { fc_rider_id }")
                return rider[2]

    for rider in riders[1:]:
        if unidecode(rider[4].lower()) == unidecode(name.lower()):
            if len(rider) == 9:
                # print(f"Length of rider is 9, so I'm adding the fc_rider_id to the list")
                # I want to add the firstcycling rider_id to the list of riders
                rider.append(fc_rider_id)
                process_files.write_csv_file('all_riders_cqranking_with_fc_rider_id.csv', riders)
            else:
                print(f"Length of rider is {len(rider)}, so I'm not adding the fc_rider_id to the list")
            return rider[2]
    """
    If we get here, the names aren't exactly the same. 
    This means it's a bit harder to find, let's step up our game.
    We have got year_of_birth and country. 
    Country are the first three character in UCICode, year of birth the next 4.
    So, let's try to find a match on that.
    Once we find a match, we see if parts of the name are in the Full name.
    """
    for rider in riders[1:]:
        parts = name.split()
        if unidecode(parts[0].lower()) in unidecode(rider[4].lower()) and unidecode(parts[1].lower()) in unidecode(rider[4].lower()):
            if len(rider) == 9:
                # I want to add the firstcycling rider_id to the list of riders
                rider.append(fc_rider_id)
                process_files.write_csv_file('all_riders_cqranking_with_fc_rider_id.csv', riders)
            else:
                print(f"Length of { rider[4] } is {len(rider)}, so I'm not adding the fc_rider_id to the list")
            return rider[2]
        # for part in parts:
        #     if part.lower() not in rider[4].lower():
        #         break
        # if rider[2]:
        #     return rider[2]
        # else:
    # print (f"{name} met fc_id {fc_rider_id} niet gevonden")

"""
Tour de France : 17
Vuelta a Espana: 23 
Giro d'Italia: 13
"""

def racename_to_id(name):
    if name[:4].lower() == 'tour':
        return 17
    elif name[:4].lower() == 'giro':
        return 13
    elif name[:6].lower() == 'vuelta':
        return 23
    else:
        print("Race niet gevonden, kan niet checken op First Cycling")


def stagename_to_number(name):
    stage =  name.split(':')[0].strip().lower()
    if stage[-2].isnumeric():
        stage_number = stage[-2:]
    elif stage[-1].isnumeric():
        stage_number = stage[-1:]
    else:
        stage_number = 0
    return stage_number

# assert int(stagename_to_number("Giro d'Italia, Stage 21 : Verona - Verona I.T.T.")) == 21
# assert int(stagename_to_number("Stage 20 : Belluno - Marmolada")) == 20
# assert int(stagename_to_number("21 : Verona - Verona I.T.T.")) == 21
# assert int(stagename_to_number("Giro d'Italia, Stage 1 : Budapest - Visegrad")) == 1

calendar = process_files.read_csv_file('calendar.csv')
def get_calendar(year=2023, months=[1,2,3,4]): #,5,6,7,8,9,10]):
    for month in months:
        start_url = "https://firstcycling.com/race.php?y="+str(year)+"&t=2&m="+str(month)
        print(f"Getting calendar for {start_url}")
        page = requests.get(start_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tables = soup.find_all("table", {"class": "sortTabell"})
        tablerows = tables[-1].find_all('tr')
        for row in tablerows[1:]:
            tds = row.find_all('td')
            category = tds[1].text.strip()
            if category not in ['1.2', '2.2', '1.2U', '2.2U']:
                date = tds[0].text.strip()
                race = tds[2].text.strip()
                content = tds[2].find('a').get('href').split('=')[1]
                race_id = content.split('&')[0]
                winner = tds[3].text.strip()
                string = tds[3].find('a').get('href').split('=')[1]
                rider_id = string.split('&')[0]
                # print(date, category, race, race_id, winner, rider_id)
                # here I have the data for each race
                # I can store it in a list, and write it to a file
                calendar.append([year, date,race,race_id, category, winner, rider_id])
        process_files.write_csv_file('calendar.csv', calendar)            

# get_calendar(2023, [1,2,3,4])
# get_calendar(2022, [1,2,3,4,5,6,7,8,9,10])
# get_calendar(2021, [1,2,3,4,5,6,7,8,9,10])
# get_calendar(2020, [7,8,9,10])
# get_calendar(2019, [1,2,3,4,5,6,7,8,9,10])
# get_calendar(2018, [1,2,3,4,5,6,7,8,9,10])

# print(scrape_result('Giro d’Italia, Stage 1 : Fossacesia Marina - Ortona I.T.T.','youth','2022'))
# print(scrape_result('Giro d’Italia, Stage 1 : Fossacesia Marina - Ortona I.T.T.','point','2022'))
# print(scrape_result('Giro d’Italia, Stage 1 : Fossacesia Marina - Ortona I.T.T.','mountain','2022'))
# scrape_result('Giro d’Italia, Stage 1 : Fossacesia Marina - Ortona I.T.T.','youth','2022')
