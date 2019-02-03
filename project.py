# Peut prendre plusieurs minutes si les pages des jeux chargent des vidéos directement 

# Imports
from selenium import webdriver
from pymongo import MongoClient

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
R = 3 # nombre de pages recherchées
all_games_info = list()
for i in range(R):
        j = 0
    
        # Recherche du nombre de jeux sur la page (25 normalement)
        all_titles = chrome.find_elements_by_class_name("title")
        print("Nombre de jeux : ", len(all_titles))

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
                        
                        jeu_actu[data[0]] = data[1]
                        print (jeu_actu)

                # Gestion des doublons
                try :
                        if( (collec.find( { 'Titre' : jeu_actu["Titre"] } ).count() == 0) and (jeu_actu not in all_games_info)):
                                all_games_info.append(jeu_actu)
                except:
                        print('Erreur Doublon')
                # Retour à la page des nouveautés
                chrome.back()

        # Déplacement vers la prochaine page
        next_page = chrome.find_element_by_xpath("//*[@id='search_result_container']/div[3]/div[2]/a[4]")
        next_page.click()

# Insertion dans la base de données de tous les éléments scrappés
if(len(all_games_info) != 0):
        db.collection_steam.insert_many(all_games_info)
        print('Ajout de ' + len(all_games_info) + ' nouveaux jeux dans la base données')


