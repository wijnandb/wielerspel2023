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


