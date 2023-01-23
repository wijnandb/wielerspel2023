"""
This is where the HTML files are being generated.

- ranking
- riders (including teamcaptains, points and JPP)
- results (including points and JPP)

At first we'll just create three HTML files, without connection between them.

Later on, we can see if we want them to be linked together.

So, let's create HTML from:
../ranking/
"""
import csv
import os

def create_html_file(input, output):
    with open(input, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    fileout = open("html/"+output, "w")

    table = "<html>\n\t<head>\n\t\t<title>Stand Wielerspel 2023</title>\n\t</head>\n\t<body>\n\t\t<table>\n"

    # Create the table's column headers
    header = data[0]
    table += "\t\t\t<tr>\n"
    for column in header:
        table += "\t\t\t\t<th>{0}</th>\n".format(column.strip())
    table += "\t\t\t</tr>\n"

    # Create the table's row data
    for row in data[1:]:
        table += "\t\t\t<tr>\n"
        for column in row:
            table += "\t\t\t\t<td>{0}</td>\n".format(column.strip())
        table += "\t\t\t</tr>\n"

    table += "\t\t</table>\n\t</body>\n</html>"

    fileout.writelines(table)
    fileout.close()

    print("HTML file gegenereerd")

import os
entries = os.listdir('CSV/')

for entry in entries:
    # print(entry)
    output = entry[:-4]+".html"
    # print(output)
    create_html_file("CSV/"+entry, output)