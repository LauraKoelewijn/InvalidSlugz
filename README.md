# RailNL

Er moet een lijnvoering gemaakt worden voor de intercitytreinen in Nederland. Dit moet binnen drie uur gebeuren met maximaal twintig trajecten. Het doel is om een lijnvoering te bedenken met zo min mogelijk treinen en een zo kort mogelijke duur die over zo veel mogelijk connecties rijdt.

## Vereisten
Onze code is geschreven in python 3.8. Om alle packages te downloaden die nodig zijn voor het runnen van de code, en in de versie die wij gebruikt hebben, run:

    pip install -r requirements.txt

## Gebruik

Het programma kan gerund worden door aanroepen van

    python main.py

Hiermee wordt de cvs file geproduceerd in de map output, genaamd output.csv waarin de lijnvoering die ons beste algoritme heeft gemaakt, wordt gepresenteerd met de uitkomst van de objective function op de onderste line.
Verder wordt er een visualisatie gemaakt van de lijnvoering met alle connecties in het zwart en de gemaakte lijnvoering in verschillende kleuren. Deze wordt geopend in een pop-up en opgeslagen in output/NL/visualisations.

### Experimenten

Het is mogelijk om in main.py verschillende stukken code uit te "commenten". Boven de stukken code staat aangegeven aan wat de code doet. Door bepaalde stukken code te runnen worden verschillende algoritmen aangeroepen en wordt er vervolgens output gegenereerd in de vorm van een boxplot of een lijngrafiek. Uit de output blijkt de kwaliteit, de K-waarde, van het programma met gegeven algoritme. Uit de verschillende outputs blijkt dat bepaalde algoritmes zorgen voor hogere K-waardes dan anderen.

## Structuur
- **/data:** bevat alle data nodig om de code te runnen
    - **/data/background:** bevat de achtergrond afbeeldingen voor de visualisatie
    - **/data/case_data:** bevat de cvs files met de stations en connecties van Holland en Nederland
    - **/data/geodata:** bevat geografische data van Holland Nederland
- **/output:** bevat alle output van de algoritmen
    - **/output/Holland:** bevat de output van de holland case
        - **/output/Holland/Baseline:** bevat de histogrammen met de analyse van de baseline (random algoritme)
        - **/output/Holland/Boxplots:** bevat boxplots waarin de uitkomst van verschillende algoritmen vergeleken worden
    - **/output/NL:** bevat de output van de NL case
        - **/output/NL/Baseline:** bevat de histogrammen met de analyse van de baseline (random algoritme)
        - **/output/NL/Boxplots:** bevat boxplots waarin de uitkomst van verschillende algoritmen vergeleken worden
        - **/output/NL/Lineplot:** bevat lineplot van de hillclimber met verschillende algoritmes
        - - **/output/NL/Visualisations:** bevat visualisatie van de gemaakte trajecten op de kaart van Nederland
- **/program:** bevat alle code voor het project
    - **/program/algorithms:** bevat de files waarin onze algoritmen zijn geschreven
    - **/program/analysis_visualisation:** bevat code voor het visualiseren en analyseren van de uitkomsten van de algoritmes
    **/program/representation:** bevat de representatie van de case


## Auteurs
Wij zijn de Invalud Slugz :snail:
- Sacha Gijsbers
- Laura Koelewijn
- Meike Klunder
