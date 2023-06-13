"""
On last day of a Grand Tour, we need to make a correction for the points earned
by winning a jersey with the poinst earned wearing that same jersey.
The scheduling is (relatively) easy, we canmake a separate schedule for this
on the last day of a GT. The problem is that we need to know the points earned
by wearing a jersey. This is not available in the results of first_cycling.
So, we look at the winner of the jersey, then we look how many times he has worn
that jersey during that GT.
"""
import datetime
import first_cycling, process_files
from decimal import *

today = datetime.date.today()

def points_earned_for_wearing_jersey(tour_id, jersey, rider_id, rider):
    """ I am getting this from the results file.
    So I guess I open it, look for the rider_id, the race_id and the position
    """
    if jersey == "gc":
        position = -4 
    elif jersey == "youth":
        position = -1
    elif jersey == "points":
        position = -2
    elif jersey == "mountain":
        position = -3
    else:
        l=jersey

    results_with_points = process_files.read_csv_file("results_with_points.csv")
    # print(results_with_points)
    points = 0
    for result in results_with_points[1:]:
        if int(result[0]) == int(position):
            # print(f"Found position: {result[0]}")
            if int(result[5]) == int(rider_id):
                # print(f"Found rider: {result[5]}")

                points = points + Decimal(result[6])
                # rider = result[4]
                ploegleider = result[9]
    if points > 0:
        """ The winner of the jersey has earned points for wearing the jersey.
        This is the amount we need to substract"""
        points = -points
        # print(0, "GTc", "Correctie voor dragen en winnen trui in Grote Ronde", tour_id, rider, rider_id, points)
        results_with_points.append([0, "GTc", "Correctie voor dragen en winnen " + jersey + " trui in Grote Ronde", rider, rider_id, points,0,today,ploegleider])
        # print(results_with_points[-1])


def determine_jersey_winner(tour_id, jersey, year="2023"):
    """
    This is the rider that wears the jersey after the last stage of the GT.
    Will I get this from FirstCycling or from CQranking?
    """
    url = "https://firstcycling.com/race.php?r="+ tour_id +"&y=2023&e=0"
    #print(url)
    if str(today) == "2023-05-26":
        rider_id, rider = first_cycling.winner_of_jersey(tour_id, jersey, year)
        points_earned_for_wearing_jersey(tour_id, jersey, rider_id, rider)

# print(points_earned_for_wearing_jersey("13", "youth", 26482, "Almeida"))
# print(points_earned_for_wearing_jersey("13", "points", 29359, "MILAN Jonathan"))
# print(points_earned_for_wearing_jersey("13", "mountain", 13080, "PINOT Thibaut"))

