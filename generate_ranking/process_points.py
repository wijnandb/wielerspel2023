from decimal import *
import process_files, count_riders

def add_points_to_results(input, output):
    """
    Add points to results, both for all_results as well as for new_results.
    If you change order or number of columns, only have to adjust it here
    """
    points = process_files.read_csv_file('points.csv')
    results = process_files.read_csv_file(input)

    for result in results[1:]: # skip the header row
        for point in points[1:]:
            if (int(result[0]) == int(point[1])) and (result[1] == point[0]):
                result[6] = Decimal(point[2])
                result[7] = int(point[3])
        #print(result)
    """
    Instead of writing the results to a file, I can also return the list with results to further process
    """
    process_files.write_csv_file(output, results)
    return True


def trigger_correction_GT():
    """
    The actual function to determine correction points is in correction_GT.py
    """
    pass


def calculate_jpp():
    """
    Look up the JPP for all team_captains.
    Determine who has the most points, second most points, etc.
    Grant the number of points to the team captain.
    Add them to the ranking
    """
    # open ranking.csv
    ranking = process_files.read_csv_file('ranking.csv')
    # open the jackpot distribution from jpp.csv
    jpp_bonus = process_files.read_csv_file('jpp.csv')
    # order ranking by JPP descending
    ranking.sort(key=lambda x: x[4], reverse=True)
    for i in range (1,14):
        ranking[i][5] = jpp_bonus[i][2]
        ranking[i][6] = Decimal(ranking[i][3]) + Decimal(ranking[i][5])
        print(ranking[i])

    ranking = redistribute_jpp_equals(ranking)
    ranking.sort(key=lambda x: x[3], reverse=True)
    print(ranking)
    # write ranking to ranking.csv
    process_files.write_csv_file('ranking.csv', ranking)
    

def redistribute_jpp_equals(data):
    jpp_values = [int(row[4]) for row in data[1:]]  # Extract JPP values as integers
    print(jpp_values)
    jpp_counts = {value: jpp_values.count(value) for value in jpp_values if jpp_values.count(value) > 1}  # Count occurrences of each JPP value
    print(jpp_counts)

    bonus_map = {}

    for row in data[1:]:
        jpp = int(row[4])
        if jpp in jpp_counts:
            if jpp not in bonus_map:
                jpp_bonus_sum = sum([Decimal(r[5]) for r in data[1:] if int(r[4]) == jpp])
                jpp_bonus_avg = jpp_bonus_sum / jpp_counts[jpp]
                bonus_map[jpp] = round(jpp_bonus_avg, 2)
            row[5] = str(bonus_map[jpp])

    total_bonus = sum([Decimal(row[5]) for row in data[1:]])
    bonus_correct = total_bonus == Decimal('75.01')

    print("Updated data:")
    for row in data:
        print(row)

    print("Total bonus is still 75.01:", bonus_correct, "It is now:", total_bonus)

    return data
