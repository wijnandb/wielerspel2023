import csv
"""
WIP. Giro is hardcoded, I should run this for all the GTs and I could run it for every race to come.
It's even possible to schedule when this script should run, because we have the date for each race

"""
race = "giro"
race_id = "13"

# read the CSV file
with open('_data/startlist-filtered.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)
    # Filter the data by race_id equal to 13
    filtered_data = [row for row in data if row['race_id'] == race_id]
    # Sort the data by team_captain in ascending order and price in descending order
    sorted_data = sorted(filtered_data, key=lambda x: (x['team_captain'], -float(x['price'])))

    # create a dictionary to store the data by team captain
    data = {}
    for row in sorted_data:
        team_captain = row['team_captain']
        price = float(row['price'])
        if team_captain in data:
            data[team_captain]['riders'].append(row)
            data[team_captain]['price'] += price
        else:
            data[team_captain] = {'riders': [row], 'price': price}
    
# generate the HTML output
output = '---\nlayout: default\ntitle: Aantal en punten per poegleider\npermalink: /startlijsten/'+race+'/\n---\n\n'
output += '{% include startlist-links.html %}\n\n'
output += '<table class="table table-striped">\n'
for team_captain, team_data in data.items():
    riders = team_data['riders']
    num_riders = len(riders)
    if num_riders != 1:
        noun = 'renners'
    else:
        noun = 'renner'
    total_price = team_data['price']
    output += f'\t<tr><td colspan="2"><h3>{team_captain}</h3></td><td><h3>{num_riders} {noun}</h3></td><td colspan="2"><h3>{int(total_price)} punten</h3></td></tr>\n'
    for rider in riders:
        start_number = rider['start_number']
        name = rider['rider']
        team = rider['team']
        country = rider['country']
        price = rider['price']
        output += f'\t<tr><td>{start_number}</td><td>{name}</td><td>{team}</td><td>{country}</td><td>{price}</td></tr>\n'
output += '</table>\n\n'

# write the output to an HTML file
with open('startlist/riders.html', 'w') as htmlfile:
    htmlfile.write(output)
