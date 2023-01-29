import process_files

teamcaptains = process_files.read_csv_file("teamcaptains.csv")
riders = process_files.read_csv_file("ploegen.csv")

def add_full_name(shortcode):
    """
    We want to display the full names of teamcaptains instead of the shortname.
    We need the short name though, because it acts as a key to the riders (teams).
    Because we need the key in the Liquid files (HTML), we can't replace them but need to add them.
    Since we also want to add the name of a temacaptain to a result, we can add the teamcaptain 
    to the last position of each line. We can only do this if the shortname has already been
    added.
    """
    # read ploegleiders_volledige_naam.csv
    # input is shortcode, output is full_name
    for tc in teamcaptains:
        if tc[0] == shortcode:
            return tc[1]



def add_teamcaptain(infile, outfile=None):
    """
    This looks up a rider from a result, then looks up the corresponding teamcaptain
    and adds the teamcaptain to the result.
    This will be the shortname of the teamcaptain, which functions as the key.
    """
    """
    Which way should I loop: which is the outer loop and which is the inner loop?

    """
    results = process_files.read_csv_file(infile)
    # add new column to results
    if results[0][-1] != "ploegleider":
        results[0].append("ploegleider")

    for result in results[1:]:
        #print(f"checking result {result}")
        result.append("niet verkocht")
        for rider in riders[1:]:
        # look up the rider in the results
            if int(result[5]) == int(rider[0]):
                # add the shortcode of the teamcaptain
                result[-1]=(rider[3])
                break
    print(results)

    process_files.write_csv_file(outfile, results)
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


