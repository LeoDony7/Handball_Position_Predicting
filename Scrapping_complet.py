from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

## On cherche à récupérer les données de match des joueurs de handball de LNH pour la saison 2023-24
## Les données se trouvent sous forme d'un tableau sur le site de la LNH
## La particularité est que le tableau n'affiche que 50 joueurs à la fois et il faut donc naviguer entre différentes pages pour récupérer toutes les données


## Configuration

# Configuration du navigateur
driver = webdriver.Chrome()

# Dictionnaire pour stocker les données (pratique pour faire un DataFrame ensuite)
dico_joueurs = dict()

# Compteur pour suivre la naviguation entre les pages
page_suivante = 2

# Ouvrir la première page
driver.get("https://www.lnh.fr/liquimoly-starligue/stats/joueurs?seasons_id=36#stats")


## Boucle sur les pages

# Pour chaque page, on va scrapper les données puis demander à Selenium de cliquer sur le bouton qui permet d'aller à la page suivante
while page_suivante <= 8 :
    # Le tableau fait seulement 7 pages, donc quand la page suivante est la 8ème, c'est qu'on arrive au bout de la boucle

    # On laisse du temps à la page pour se charger afin que Selenium fonctionne sans soucis
    time.sleep(3)

    # Extraire le HTML actuel et le parser avec BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Récupération du nom des colonnes sur la première page  
    if page_suivante ==2:
        entete = soup.find('thead')
        entete_noms = entete.find_all('th')
        entete_formate = [nom.text.strip() for nom in entete_noms] 
    # On récupère une liste contenant le nom de chaque colonne du tableau, dans un format str classique
    # Cette liste sera utilisée pour renommer les colonnes au moment de la création du DataFrame pandas

    # Scrapping des données de la page pour les mettre dans le dictionnaire
    table = soup.find('table', {'class': 'table-stats'})
    rows = table.find_all('tr')[1:]

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols)>0 :
           dico_joueurs[" ".join(cols[0].lstrip('0123456789\n').split())] = cols[1:]
           # On met directement le nom des joueurs dans un format lisible au moment de créer le dictionnaire


    # Trouver et cliquer sur le bouton "Page suivante"

    if page_suivante <=7 : # On ne veut passer à la page suivante que si on n'est pas déjà à la dernière (afin d'éviter des erreurs d'éxécution)
        
        # Balise HTML du bouton permettant de passer à la page suivante
        selecteur_bouton = f"//a[contains(@class, 'pagination-bt') and @name='{page_suivante}']"
    
        # On demande à Selenium de trouver le bouton et de cliquer dessus
        # Voir si on peut pas réécrire ca sans les levées d'exception et d'erreurs, car elles sont pas censées arriver
        try:
            next_button = driver.find_element("xpath", selecteur_bouton)
            if "disabled" in next_button.get_attribute("class"):
                break  # Quitter si le bouton "Page suivante" est désactivé
            next_button.click()
        except Exception as e:
            ("Fin des pages ou problème détecté :", e)
            break
    
    # Mise à jour du compteur de page
    page_suivante+=1

## Fin de la boucle While sur les pages


# Fermer le navigateur
driver.quit()


## Récuperation des données sous forme d'un fichier csv
## Afin de ne pas avoir à scrapper à nouveau les données à chaque fois

# Création du DataFrame à partir du dictionnaire
data_joueurs = pd.DataFrame.from_dict(dico_joueurs, orient="index")

# Renommage des colonnes
data_joueurs.columns = entete_formate[1:]

# Nom complet du fichier (nom et chemin)
# A modifier si vous souhaiter scrapper vous même les données et les enregistrer sur votre machine
nom_fichier = os.path.join("C:\\", "Leo_Perso", "ENSAE", "2A", "S1", "PythonDS", "Projet_DS_Handball","data_joueurs_complet4.csv")

# Enregistrement du tableau au format csv en gardant l'index (nom des joueurs)
data_joueurs.to_csv(nom_fichier, index= True)




