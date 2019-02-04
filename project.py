# Peut prendre plusieurs minutes si les pages des jeux chargent des vidéos directement et si le nombre de pages scrapées est grand

# Imports
from selenium import webdriver
from pymongo import MongoClient
import datetime


# Nombre de pages à rechercher : chaque page contient 25 jeux normalement (conseil : mettre entre 1 et 3 pour voir les fonctionnalités rapidement)
R = 1

# Fonction de mapping rapide des équivalences mois-numéros
def month_test(x):
    return {
        'janv.': '01',
        'févr.': '02',
        'mars': '03',
        'avr.': '04',
        'mai': '05',
        'juin': '06',
        'juil': '07',
        'août': '08',
        'sept.': '09',
        'oct.': '10',
        'nov.': '11',
        'déc.': '12',
    }[x]

# Fonction de validation du format de la date
def validate_time(date_text):
    try:
        date = datetime.datetime.strptime(date_text, '%d-%m-%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be DD-MM-YYYY")

    return date

# Fonction de transformation des dates scrapées en format de date utilisable
def modif_date(date_text):
    date_end = ''
    date_time = date_text.split(" ")
    try:
        day = date_time[0]
        month = date_time[1]
        year = date_time[2]

        month_number = month_test(month)
        all_date = str(day)+'-'+str(month_number)+'-'+str(year)
        date_end = validate_time(all_date)

    except:
        return ""

    return date_end



# Création du client Mongo pour se connecter à la base de données
client = MongoClient('mongodb://localhost:27017/')

db = client.database_steam
collec = db.collection_steam

# Création du webdriver
chrome = webdriver.Chrome(executable_path="chromedriver.exe")

# Déplacement vers le site
chrome.get("https://store.steampowered.com/?l=french")

# Déplacement vers la catégorie Jeux
link_jeux = chrome.find_element_by_link_text("Jeux")
link_jeux.click()

# Déplacement vers la catégorie Nouveautés
link_new = chrome.find_element_by_link_text("Parcourir toutes les nouveautés")
link_new.click()

i = 0 # compteur boucle / Chaque page globale
j = 0 # compteur boucle 2 / Chaque jeu sur la page
all_games_info = list()
for i in range(R):
        j = 0
    
        # Recherche du nombre de jeux sur la page (25 normalement)
        all_titles = chrome.find_elements_by_class_name("title")
        #print("Nombre de jeux : ", len(all_titles))

        # Boucle sur le nombre de jeux
        for j in range(len(all_titles)):
                print(j)
        
                # Déplacement vers la page spécifique du jeu
                x = j+1
                link_game = chrome.find_element_by_xpath("//*[@id='search_result_container']/div[2]/a["+ str(x) + "]")
                link_game.click()

                # Scrapping des infos sur la page
                try : 
                        infos = chrome.find_elements_by_class_name("details_block")
                except :
                        print('Erreur Block')
                        continue
                
                i = infos[0]

                liste_i = i.text.splitlines()
                jeu_actu = dict()
                for x in liste_i:
                        data = x.split(" : ")

                        # Récupération des informations recherchées
                        if((len(data) != 2) | (data[0] not in ["Titre", "Genre", "Développeur", "Éditeur", "Date de parution"])):
                                continue
                        
                        if(data[0] == "Date de parution"):
                                jeu_actu["Datetime"] = modif_date(data[1])
                        else:
                                jeu_actu["Datetime"] = ""

                        jeu_actu[data[0]] = data[1]

                # Gestion des doublons
                try :
                        if( (collec.find( { 'Titre' : jeu_actu["Titre"] } ).count() == 0) and (jeu_actu not in all_games_info)):
                                all_games_info.append(jeu_actu)
                except:
                        print('Erreur Page du jeu')
                # Retour à la page des nouveautés
                chrome.back()

        # Déplacement vers la prochaine page
        next_page = chrome.find_element_by_xpath("//*[@id='search_result_container']/div[3]/div[2]/a[4]")
        next_page.click()

# Insertion dans la base de données de tous les éléments scrappés
if(len(all_games_info) != 0):
        db.collection_steam.insert_many(all_games_info)
        print('Ajout de ' + str(len(all_games_info)) + ' nouveau(x) jeu(x) dans la base de données')


