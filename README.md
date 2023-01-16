# RailNL

Er moet een lijnvoering gemaakt worden voor de intercitytreinen in Noord-Holland. Hierbij moeten alle connecties tussen de gegeven stations minimaal één keer bereden worden. Dit moet binnen twee uur gebeuren met maximaal zeven trajecten. Het doel is om een lijnvoering te bedenken met zo min mogelijk treinen en een zo kort mogelijke duur.

## Gebruik

Het programma kan gerund worden door aanroepen van 

    python main.py

Hiermee wordt de cvs file geproduceerd, genaamd output.csv waarin de lijnvoering die het algoritme heeft gemaakt, wordt gepresenteerd met de uitkomst van de objective function op de onderste line.
Verder wordt er een visualisatie gemaakt van de lijnvoering met alle connecties in het zwart en de gemaakte lijnvoering in verschillende kleuren. Deze wordt geopend in een pop-up en opgeslagen.

## Structuur
- **/data** bevat de cvs files met de data over het probleem
- **/output** hierin worden het csv bestand met de lijnvoering en de visualisatie opgeslagen
- **/program/** bevat alle code voor het project

** TO DO** leg de structuur van de code uit, en als we vereisten hebben.

## Auteurs

- Sacha Gijsbers
- Laura Koelewijn
- Meike Klunder