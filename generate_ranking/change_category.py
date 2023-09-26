"""
Some categories are different on CQranking from what we want to use in our Wielerspel.
All of these categories are in the 1.UWT and 2.UWT UCI categories. See 
https://docs.google.com/spreadsheets/d/1xlh_-Prhsf0-E5q7bGRJG-6lejCff3Bn/edit#gid=838025687
for an overview.

I think we'll have to do a text comparison and based on that change the category.
This means category changes for the following races:

Omloop het Nieuwsblad -> 1.WT2
Strade Bianche -> 1.WT2

Volta a Catalunya -> 2.WT1
Itzulia Basque Country 2.WT1
Tour de Pologne -> 2.WT1
Benelux Tour -> 2.WT1

Amstel Gold Race -> 1.WT1

I can look for the name of the race and based on that change it, or I can look up
the race_id, which would mean I need to change my code next year.

Let's go for finding the name.

I send the racename to this function, and then return the (new) category.
"""

def new_category(racename,category):
  if racename[:14] in ['Omloop Het Nie','Strade Bianche']:
    category = '1.WT2'
  if racename[:16] in ['Amstel Gold Race']:
    category = '1.WT1'
  # if racename in ['Volta a Catalunya','Itzulia Basque Country','Tour de Pologne','Benelux Tour']:
  #   category = '2.WT1'
  if racename[:11] in ['Volta a Cat','Itzulia Bas','Tour de Pol','Renewi Tour']:
    if category == '2.WT2':
      category = '2.WT1'
    else:
      category = '2.WT1s'
  return category
