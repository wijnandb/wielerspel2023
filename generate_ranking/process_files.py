import csv


def read_csv_file(filename):
    """
    Function to read CSV files, being called from (by) other functions
    WIP: Directory is hardcoded in function!!
    """
    file = '_data/'+str(filename)
    with open(file, newline='') as f:
        readresults = csv.reader(f)
        csvlist = list(readresults)
    return csvlist


def write_csv_file(filename, results):
    """
    Function to write CSV files, being called from (by) other functions
    WIP: Directory is hardcoded in function!!
    """
    file = '_data/'+str(filename)
    with open(file, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerows(results)


def write_row_in_HTML_table(row):
    start = "<tr>"
    for value in row:
        start.append("<td>"+str(value)+"</td>")
    start.append("</tr>")
    return start