import pandas as pd
from bs4 import BeautifulSoup
import os 
import time

## Téléchargement d'un DataFrame en précisant le nom et le chemin de teléchargement (optionnel)

def telechargement_DF(df:pd.DataFrame,nom_fichier,path=None):
    if path is None :
        chemin = os.getcwd()
    else:
        chemin = path
    nom_complet = os.path.join(chemin,nom_fichier)
    df.to_csv(nom_complet,index=True)

############### Fonctions pour le scrapping des données de match ###############

## Scrapping d'une page des données de match

def Scrap_page_match(driver,dictionnaire):

    '''
    La fonction prend un argument un driver et un dictionnaire. 
    Elle modifie le contenu du dictionnaire en ajoutant les informations scrappées sur la page du driver
    Cette fonction sera appliqué au driver qui visite la page de la LNH qui nous intéresse dans ce projet
    Le dictionnaire dans lequel on ajoute les informations de la page sera utilisé pour créer le DataFrame de travail
    '''

    # Extraire le HTML actuel et le parser avec BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Scrapping des données de la page pour les mettre dans le dictionnaire
    table = soup.find('table', {'class': 'table-stats'})
    rows = table.find_all('tr')[1:] # on récupère toute les lignes du tableau sous forme d'une liste

    # Puis pour chaque ligne, on récupère toutes les cases de la ligne et on ajoute les informations correspondantes dans le dictionnaire
    # On prend la première case de chaque ligne (nom du joueur) comme clé du dictionnaire et le restes des informations comme valeur pour cette clé
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols)>0 :
           dictionnaire[" ".join(cols[0].lstrip('0123456789\n').split())] = cols[1:]
           # On met directement le nom des joueurs dans un format lisible au moment de créer le dictionnaire
           # Amélioration possible en créant une fonction qui obtient ce format lisible et en l'applicant à cols[0]

## Récupération du nom des colonnes du tableau de stats de match

def nom_colonnes(driver):

    '''
    La fonction prend en argument un driver qui est un objet de type WebDriver de Selenium.
    Elle renvoie une liste contenant les noms des colonnes du tableau présent sur la page visitée par le driver
    Cette fonction sera appliqué au driver qui visite la page de la LNH qui nous intéresse dans ce projet
    La liste renvoyée par cette fonction a pour vocation de devenir le nom des colonnes du DataFrame contenant les données de cette page
    '''

    # Extraire le HTML actuel et le parser avec BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Récupétation de la tête du tableau, qui contient les informations qu'on recherche
    entete = soup.find('thead')
    entete_noms = entete.find_all('th')
    entete_formate = [nom.text.strip() for nom in entete_noms]
    return entete_formate

## Cliquer sur le bouton amenant à la page suivante

def page_suivante(driver,next_page):

    '''
    
    '''

    # Balise HTML du bouton permettant de passer à la page suivante
    selecteur_bouton = f"//a[contains(@class, 'pagination-bt') and @name='{next_page}']"

    # On demande à Selenium de trouver le bouton et de cliquer dessus
    next_button = driver.find_element("xpath", selecteur_bouton)
    next_button.click()
    # Fonction écrite sans gérer les potentielles erreurs qui pourraient arriver

#########

def Scrap_page_joueur(driver,url,dictionnaire):
        
        '''
        La fonction prend un argument un driver,un url et un dictionnaire. 
        Elle modifie le contenu du dictionnaire en ajoutant les informations scrappées sur la page du driver
        Cette fonction sera appliqué au driver qui visite la page d'un joueur de LNH
        L'url passé en argument sera celui de la page du joueur qui nous intéresse
        Le dictionnaire dans lequel on ajoute les informations de la page sera utilisé pour créer le DataFrame de travail
        '''        

        # Récupérer le code source HTML après le rendu JavaScript
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Scrapping de l'élément dans lequel se trouve les informations
        table = soup.find('div', {'class': 'col-infos'})

        if table:

            '''
            Ajout d'une condition pour faire face aux pages de joueurs manquantes
            Si la page joueur existe on effectue la suite du scrapping
            Dans le cas contraire on ajoute seulement la clé 'url' au dictionnaire, associée à la valeur []
            Cela permet d'ajouter une ligne au dataframe même pour les joueurs dont la page est manquante
            '''

            ## Coeur du Scrapping
            nom_joueur = table.find('h2').text.strip() 
            poste_joueur = table.find('div',{'class':'position'}).text.strip() 
            rows = table.find_all('div',{'class':'row-infos'})

            # Ajout des données au dictionnaire
            valeur=[poste_joueur] 

            # le poste du joueur n'est pas renseigné de la même façon que les autres données donc on l'ajoute à la main avant les autres informations
            for row in rows:
                information_brute = row.find('div',{'class' : 'col-value'})
                if information_brute : 
                    information = information_brute.text.strip()
                    valeur.append(information) 

            dictionnaire[" ".join(nom_joueur.split())] = valeur
        
        else:
            dictionnaire[url]=[]

#########

def entete_infos_joueur(driver):
    
    '''
    Cette fonction prend en argument un driver.
    Elle renvoie une liste contenant le nom des colonnes du tableau dans lequel sont les données d'un joueur.
    Cette fonction sera appliquée au driver qui visite la page d'un joueur (en particulier on l'appliquera sur la page du premier joueur du tableau).
    La liste renvoyée sera utilisée pour renommer les colonnes du dataframe comprenant les données des joueurs.
    '''

    # Récupérer le code source HTML après le rendu JavaScript
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Scrapping de l'élément contenant les informations voulues
    table = soup.find('div', {'class': 'col-infos'})
    rows = table.find_all('div',{'class' : 'row-infos'})

    # Récupération du nom des colonnes (on récupère à la main le poste puisque sur la page l'affichage n'est pas le même)
    labels =["poste"]
    for row in rows:
        nom_colonne_brut = row.find('div', {'class' : 'col-label'})
        if nom_colonne_brut :
            nom_colonne = nom_colonne_brut.text.strip()
            labels.append(nom_colonne)
    
    # Ajout du nom de la dernière colonne 
    # Pour certains joueurs est rajouté sur la page quelle saison est leur dernière
    # Comme ce n'est pas le cas sur la page du premier joueur, on rajoute à la main
    if len(labels)==7:
        labels.append("Dernière saison")

    return labels

#########

def Scrap_url_page(driver):

    '''
    La fonction prend en argument un driver.
    Elle renvoie une liste de liens de pages internet
    Cette fonction sera utilisée sur le driver qui visite la page de la LNH qui nous intéresse
    La liste d'url renvoyé sera utilisé pour aller sur la page de chaque joueur afin d'en scrapper les informations
    '''

    # Extraire le HTML actuel et le parser avec BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Scrapping de la liste des url
    liste_joueurs_brute = soup.find_all('div',{'class':'name'})
    liste_joueurs = [joueur.find('a') for joueur in liste_joueurs_brute]
    liste_url = [joueur['href'] for joueur in liste_joueurs]

    return liste_url

#########

def page_joueur(driver,url):

    '''
    Cette fonction prend un driver et un url en argument
    Elle emmène le driver sur la page correspondante à l'url en cliquant sur l'élément amenant à cette page
    La fonction sera appliqué à la page de la LNH qui nous intéresse
    Elle sera utilisée pour nous amener sur la page d'un joueur dont on souhaite récupérer les données
    '''

    # On cherche le lien qui nous amène à la page du joueur depuis la page des stats de match
    element = driver.find_element('xpath',f"//a[@href='{url}']")

    # On scrolle jusqu'à l'élément pour pas avoir de pb durant la visite de la page 
    position_clique = driver.execute_script("return arguments[0].offsetTop;", element)
    driver.execute_script(f"window.scrollTo(0, {position_clique});")

    # On clique sur le lien   
    element.click()

########

def Scrap_tableau_joueur(driver,dictionnaire,liste_labels):

    '''
    Cette fonction prend en argument un driver, un dictionnaire et une liste.
    Elle modifie le dictionnaire en le remplissant avec les données des pages des joueurs présents sur la page.
    La fonction récupère également le nom des colonnes de la table contenant les données et les ajoute à la liste
    La fonction sera appliquée à la page de la LNH qui nous intéresse.
    Le dictionnaire et la liste de labels finaux seront utilisés pour construire un dataframe de travail
    '''

    # Récupération de la liste des url vers les pages joueurs de la page
    liste_url = Scrap_url_page(driver)

    # Boucle sur toutes les pages à scrapper
    for url in liste_url :

        # On va sur la page du joueur correspondant à l'url
        page_joueur(driver,url)

        # Temps d'attente pour s'assurer que la page est bien chargée avant de commencer le scrapping
        driver.implicitly_wait(10) 

        # Si lon ne l'a pas déjà fait, on récupère le nom des colonnes
        if len(liste_labels)<=7:
            liste_labels.extend(entete_infos_joueur(driver))

        # On scrappe les données de la page 
        Scrap_page_joueur(driver,url,dictionnaire)

        # Retour à la page précédente (celle avec le tableau de joueurs)
        driver.back()

        # Temps d'attente pour s'assurer que la page est bien chargée avant de passer au joueur suivant
        time.sleep(2)





