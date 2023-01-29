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



def add_teamcaptain(results):
    """
    This looks up a rider from a result, then looks up the corresponding teamcaptain
    and adds the teamcaptain to the result.
    This will be the shortname of the teamcaptain, which functions as the key.
    """
    """
    Which way should I loop: which is the outer loop and which is the inner loop?
    
    """
    for rider in riders:
        for result in results:
            # look up the rider in the results
            if result[] == rider[]:
                # add the shortcode of the teamcaptain
                result.append(rider[])
    """
    Doing it the other way around makes it possible to add "not sold" to a rider
    """

