"""
Processing consists of several steps:

-  add points to results

- add up points per rider

- add up points per teamcaptain

- sort teamcaptains by points and JPP
"""
import csv
import operator
from decimal import *
#from datetime import datetime
"""
results.csv
0 - rank
1 - category
2 - racename
3 - race_id
4 - rider_name
5 - rider_rider_id
6 - points
7 - JPP
"""
def read_csv_file(filename):
    file = '_data/'+str(filename)
    with open(file, newline='') as f:
        readresults = csv.reader(f)
        csvfile = list(readresults)
    return csvfile

"""
points.csv:
0 - racecategory
1 - ranking
2 - points
3 - jpp
"""

def add_points_to_results():
    points = read_csv_file('points.csv')
    results = read_csv_file('all_results.csv')

    for result in results[1:]: # skip the header row
        for point in points:
            if (int(result[0]) == int(point[1])) and (result[1] == point[0]):
                result[6] = Decimal(point[2])
                result[7] = int(point[3])
        #print(result)
    """
    Instead of writing the results to a file, I can also return the list with results to further process
    """
    write_csv_file('results_with_points.csv', results)
    return True


def write_csv_file(filename, results):
    file = '_data/'+str(filename)
    with open(file, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(results)


def get_teamcaptains(sold_riders):
    teamcaptains = []
    for sr in sold_riders[1:]:
        if sr[3] not in teamcaptains:
            teamcaptains.append(sr[3])
    return teamcaptains


"""
ploegen.csv
0 - renner_id
1 - rider_name
2 - rider_full_name
3 - teamcaptain
4 - price
5 - team
6 - nationality
7 - age
8 - points
9 - JPP
"""

def add_up_points_per_rider():
    riders = read_csv_file("ploegen.csv")
    results = read_csv_file("results_with_points.csv")

    for rider in riders[1:]:
        points = 0
        JPP = 0
        for result in results[1:]:
            if rider[0] == result[5]:
                points += Decimal(result[6])
                JPP += int(result[7])
        rider[8] = Decimal(points)
        rider[9] = int(JPP)
        # if rider[8] > 0 or rider[9] > 0:
        #     print(f"{rider[2]}, {rider[8]} points, {rider[9]} JPP\n")
    
    # store the riders with points in a CSV
    # or progress to the next step, adding up points per teamcaptain
    write_csv_file("riders_with_points.csv", riders)
    add_up_points_per_teamcaptain(riders)


def add_up_points_per_teamcaptain(riders):
    # riders = read_csv_file("ploegen.csv")
    ranking = []
    teamcaptains = get_teamcaptains(riders)
    for teamcaptain in teamcaptains:
        team = []
        points = 0
        JPP = 0
        #print(teamcaptain)
        for rider in riders:
            if rider[3] == teamcaptain:
                # add to teamcaptain.csv
                team.append([rider])
                points += Decimal(rider[8])
                JPP += int(rider[9])
        write_csv_file("ploegleiders/"+teamcaptain+".csv", team)
        ranking.append([teamcaptain, Decimal(points),int(JPP)])

    #print(sorted(ranking))#, key=lambda x:(x[1], x[2], x[0])))
    ranking = sorted(ranking, key=operator.itemgetter(1, 2), reverse=True)
    # append headers, 
    # add rank, with i for len(ranking)
    ranking_with_rank = [['positie','ploegleider','punten','JPP']]
    for i in range(len(ranking)):
        ranking_with_rank.append([i+1, ranking[i][0], ranking[i][1], ranking[i][2]])
    
    # for r in ranking_with_rank:
    #     print(r)
    #processtime = datetime.today().strftime('%Y-%m-%d#%H:%M:%S')
    write_csv_file("ranking.csv", ranking_with_rank)


if add_points_to_results():
    print("Added points and JPP to results")
    add_up_points_per_rider()
