---
template: default
title: Uitleg en aanpak
---
Geachte deelnemers aan het Wielerspel, zie hier de automatisch gegenereerde stand.

Een aantal maal per dag wordt er op de [beginpagina van CQranking](https://cqranking.com/men/asp/gen/start.asp) gekeken of er al nieuwe uitslagen binnen zijn. 

Dit gebeurt automatisch, er draait een zogenaamde _scraper_, een klein Python programmaatje dat deze uitslagen binnenhaalt en opslaat als tekstbestandje.

Als het gaat om een etappe, een berg- of puntentrui, of een kleiner nationaal kampioenschap, dan wordt het resultaat direct binnengehaald. Gaat het om een eendags-koers of een (eind)klassement, dan kijkt de _scraper_ een niveau dieper en haalt afhankelijk van het soort wedstrijd, de top 3 (1.1 en 2.1), de top 15 (Giro en Vuelta), de top 20 (Tour de France) of de top 10 binnen (alle overige koersen).

Omdat alleen de laatste uitslagen op deze pagina staan, worden deze uitslagen vergeleken met eerder opgehaalde uitslagen, zodat we geen dubbele uitslagen verwerken.

In de volgende stap worden de punten (en JPP) aan de resultaten toegevoegd, door in weer een ander bestand de punten op te zoeken die behoren bij de positie en de category.

Dan volgt de stap waar [per renner de verdiende punten en jackpotpunten]({% link points.html %}) uit de uitslagen worden opgeteld, gevolgd door het optellen van de punten per ploegleider. 

Deze uitkomst ordenen op punten en jackpotpunten, rangorde toevoegen en we hebben de basis voor de [stand]({% link index.html %}).

Al deze files worden vervolgens naar Github _gepusht_, waar ze tot HTML files worden gegenereerd en direct worden gepubliceerd.



