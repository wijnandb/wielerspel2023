import process_files

def add_full_name(shortcode):
    """
    We want to display the full names of teamcaptains instead of the shortname.
    We need the short name though, because it acts as a key to the riders (teams).
    Because we need the key in the Liquid files (HTML), we can't replace them but need to add them.
    Since we also want to add the name of a temacaptain to a result, we can add the teamcaptain 
    to the last position of each line. We can only do this if the shortname has already been
    added.
    """
    ploegleiders = 


def add_teamcaptain():
    """
    This looks up a rider from a result, then looks up the corresponding teamcaptain
    and adds the teamcaptain to the result.
    This will be the shortname of the teamcaptain, which functions as the key.
    """
    pass


def get_teamcaptains(sold_riders):
    teamcaptains = []
    for sr in sold_riders[1:]:
        if sr[3] not in teamcaptains:
            teamcaptains.append(sr[3])
    return teamcaptains