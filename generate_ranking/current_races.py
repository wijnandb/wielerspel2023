"""
- get calendar
- filter it for upcoming races
- get startlists



"""


import process_files

import datetime

calendar = process_files.read_csv_file('calendar.csv')

today = datetime.datetime.now()

print(today)
currentweek = today.isocalendar().week
print(currentweek)
calendar_with_startdate = [[datetime.datetime.strptime(item[0], '%Y-%m-%d')] + item[1:] for item in calendar[1:]]

#races = filter(lambda x: x[0] > datetime.datetime.now(), calendar[1:])
calendar_with_dates = []
for c in calendar_with_startdate:
    if c[1] != "":
        c[1] = datetime.datetime.strptime(c[1], '%Y-%m-%d')
    calendar_with_dates.append(c)
    #print(calendar_with_dates[-1])

def is_current_race(race):
    # These are the races that are on this week
    if race[0].isocalendar().week == currentweek:
        # print(f"Eendaagse koers of start meerdaagse koerss {race}")
        return True
    elif race[1] != "":
        if race[1].isocalendar().week == currentweek:
            # print(f"Meerdaagse koers eindigt {race}")
            return True
        elif race[0].isocalendar().week < currentweek and race[1].isocalendar().week > currentweek:
            # print(f"Meerdaagse koers meer dan een week { race}")
            return True
    return False

current_races = [['startdate','enddate','race','FC_race_id','category','points','jpp']]    
for race in calendar_with_dates:
    if is_current_race(race):
        current_races.append(race)
    
process_files.write_csv_file("current_races.csv", current_races)
# Now we also want to have the races that have already started but aren't finished yet
# that means 

