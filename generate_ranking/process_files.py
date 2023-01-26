import csv


def read_csv_file(filename):
    file = '_data/'+str(filename)
    with open(file, newline='') as f:
        readresults = csv.reader(f)
        csvlist = list(readresults)
    return csvlist


def write_csv_file(filename, results):
    """
    WIP: Directory is hardcoded in function!!
    """
    file = '_data/'+str(filename)
    with open(file, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(results)