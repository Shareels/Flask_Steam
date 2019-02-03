# Flask-Mongo Steam

## Contexte

Création d'un projet mettant en oeuvre trois parties distinctes :  
-- Recueil de données (par scraping avec Selenium dans notre cas)  
-- Stockage dans une base de données MongoDB  
-- Interface Flask d'interrogation de la DB  

La partie optionnelle consistant à utiliser Docker n'est pas mise en place.  

## Sujet du projet

Nous avons cherché à récupérer des données sur le site "https://store.steampowered.com/?l=french", qui propose des fiches de jeux vidéos en ligne.  

## Installation

N'ayant pas fait de Docker actuellement, il est nécessaire d'installer les éléments suivants : 
-- MongoDB (installation windows + commande md \data\db "https://docs.mongodb.com/v3.2/tutorial/install-mongodb-on-windows/" 
OU installation linux "https://docs.mongodb.com/v3.2/administration/install-on-linux/")  
-- PyMongo (python -m easy_install pymongo OU pip install pymongo)  
-- Flask (pip install flask)  
-- Flask-PyMongo (pip install Flask-PyMongo)  
-- Flask-WTF(easy_install Flask-WTF OU pip install Flask-WTF)  
-- Selenium (pip install selenium)  

Normalement, le chromedriver utilisé par Selenium est joint au projet.  
Si ce n'est pas le cas, il suffit d'aller le télécharger ici (https://sites.google.com/a/chromium.org/chromedriver/downloads) et de le positionner dans le répertoire du projet.