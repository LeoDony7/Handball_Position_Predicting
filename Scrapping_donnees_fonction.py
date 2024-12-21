from selenium import webdriver
import time
import pandas as pd
from Fonctions_scrapping import *


def Scrapping(nom_df_match: str, nom_df_physique: str):

    '''
    Cette fonction réalise le scrapping dans son intégralité, en utilisant les fonctions du fichier "Fonctions_scrapping.py".
    La fonction scrappe les données, les regroupe dans 2 DataFrames distincts, puis télécharge ces 2 DataFrames au format csv dans le repertoire actuel.
    Elle prend donc en argument le nom que vous voulez donner aux fichiers, au format "nom_fichier.csv"
    '''

    # Configuration du navigateur
    driver = webdriver.Chrome()

    # Dictionnaire pour stocker les données (pratique pour faire un DataFrame ensuite)
    dico_match = dict()
    dico_physique = dict()

    # Labels pour le DataFrame qui contiendra les données des joueurs
    label_physique = []

    # Compteur pour suivre la navigation entre les pages
    next_page = 2

    # Ouvrir la page
    driver.get("https://www.lnh.fr/liquimoly-starligue/stats/joueurs?seasons_id=36#stats")

    # Boucle sur les 7 pages de données de la page LNH (il est plus approprié d'utiliser next_page que page comme compteur dans notre code)
    while next_page <= 8 : 

        # Temps d'attente pour s'assurer que la page est bien chargée avant de commencer le scrapping
        time.sleep(2)

        # Si première page, on récupère le nom des colonnes pour le DataFrame des données de matchs
        if next_page ==2:
            label_match = nom_colonnes(driver)

        # Scrapping des données de la page (données de matchs puis données des joueurs de la page)
        Scrap_page_match(driver, dico_match)
        Scrap_tableau_joueur(driver,dico_physique,label_physique)


        if next_page <= 7 : 
            page_suivante(driver,next_page)
    
        # Mise à jour du compteur de page
        next_page+=1

    # Fermeture du Webdriver
    driver.quit()

    # Création des 2 DataFrames avec colonnes renommées
    data_match = pd.DataFrame.from_dict(dico_match, orient='index')
    data_match.columns=label_match[1:]

    data_physique = pd.DataFrame.from_dict(dico_physique, orient='index')
    data_physique.columns=label_physique

    telechargement_DF(data_match,nom_df_match)
    telechargement_DF(data_physique,nom_df_physique)

