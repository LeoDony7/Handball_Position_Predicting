## Scrapping des données

import pandas as pd
from bs4 import BeautifulSoup
import os 
import time

## Téléchargement d'un DataFrame en précisant le nom et le chemin de teléchargement (optionnel)

def telechargement_DF(dataframe:pd.DataFrame,nom_fichier,path=None):

    '''
    Télécharge un DataFrame au format .csv selon le nom voulu.
    On peut également préciser le chemin vers le repertoire dans lequel le fichier sera téléchargé, par défaut le repertoire actuel.

    Paramètres :
        - dataframe : Un DataFrame pandas qu'on souhaite télécharger.
        - nom_fichier : Une chaine de caractère de la forme "nom_fichier.csv". Nom qu'on souhaite donner au fichier.
        - path (optionnel) : Une chaine de caractère définissant le chemin vers le dossier dans lequel le fichier sera téléchargé. Par défaut le répertoire actuel.
    '''

    if path is None :
        chemin = os.getcwd()
    else:
        chemin = path
    nom_complet = os.path.join(chemin,nom_fichier)
    dataframe.to_csv(nom_complet,index=True)


############### Fonctions pour le scrapping des données de match ###############


## Scrapping d'une page des données de match

def Scrap_page_match(driver,dictionnaire):

    '''
    Remplit un dictionnaire avec les données souhaitées de la page visitée.
    La page visitée sera celle des données de la saison 2023/24 de la LNH (Ligue Nationale de Handball)
    
    Paramètres :
        - driver : Un Webdriver selenium. On utilisera toujours un Webdriver.Chrome()
        - dictionnaire : Un dictionnaire python. Il sera rempli avec les données de la page visitée afin de créer un DataFrame.
    
    '''

    # Extraire le HTML actuel et le parser avec BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Scrapping des données de la page pour les mettre dans le dictionnaire
    table = soup.find('table', {'class': 'table-stats'})
    rows = table.find_all('tr')[1:] # on récupère toute les lignes du tableau sous forme d'une liste

    # Puis pour chaque ligne, on récupère toutes les cases de la ligne et on ajoute les informations correspondantes dans le dictionnaire
    # On prend la première case de chaque ligne (nom du joueur) comme clé du dictionnaire et le reste des informations comme valeur pour cette clé
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols)>0 :
           dictionnaire[" ".join(cols[0].lstrip('0123456789\n').split())] = cols[1:]
           # On met directement le nom des joueurs dans un format lisible au moment de créer le dictionnaire


## Récupération du nom des colonnes du tableau de stats de match

def nom_colonnes(driver):

    '''
    Renvoie le nom des colonnes du tableau de la page de la LNH sous forme d'une liste.
    Cette fonction va permettre de renommer les colonnes du DataFrame lorsqu'il sera construit.
    
    Paramètres :
        - driver : Un Webdriver selenium. On utilisera toujours un Webdriver.Chrome()
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
    Clique sur le bouton amenant à la page dont le numéro est passé en argument.
    La fonction sera utilisée pour naviguer entre les différentes pages durant le scrapping.

    Paramètres :
        - driver : Un Webdriver selenium. On utilisera toujours un Webdriver.Chrome()
        - next_page : Un entier de [1,7]. Il définit la page vers laquelle on souhaite aller.
    '''

    # Balise HTML du bouton permettant de passer à la page suivante
    selecteur_bouton = f"//a[contains(@class, 'pagination-bt') and @name='{next_page}']"

    # On demande à Selenium de trouver le bouton et de cliquer dessus
    next_button = driver.find_element("xpath", selecteur_bouton)
    next_button.click()



############### Fonctions pour le scrapping des données des joueurs ###############


## Scrapping d'une page d'un joueur

def Scrap_page_joueur(driver,url,dictionnaire):
        
    '''
    Remplit un dictionnaire avec les données de la page correspondant à l'url passé en argument.
    La page visitée sera celle d'un joueur de la LNH pendant la saison 2023/24.

    Paramètres :
        - driver : Un Webdriver selenium. On utilisera toujours un Webdriver.Chrome()
        - url : Une chaine de caractère de la forme "https://www.lnh.fr/liquimoly-starligue/joueurs/prenom-nom". Page du joueur dont on souhaite récupérer les données.
        - dictionnaire : Un dictionnaire python. Il sera rempli avec les données de la page visitée afin de créer un DataFrame.
    '''        

    # Extraire le HTML actuel et le parser avec BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Scrapping de l'élément dans lequel se trouve les informations
    table = soup.find('div', {'class': 'col-infos'})

    if table:

        '''
        Ajout d'une condition pour faire face aux pages de joueurs manquantes.
        Si la page joueur existe on effectue la suite du scrapping.
        Dans le cas contraire on ajoute seulement la clé 'url' au dictionnaire, associée à la valeur [].
        Cela permet d'ajouter une ligne au dataframe même pour les joueurs dont la page est manquante.
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


# Récupération du nom des colonnes du tableau des données des joueurs

def entete_infos_joueur(driver):
    
    '''
    Renvoie le nom des colonnes du tableau de la page d'un joueur sous forme d'une liste.
    Cette fonction va permettre de renommer les colonnes du DataFrame lorsqu'il sera construit.
    
    Paramètres :
        - driver : Un Webdriver selenium. On utilisera toujours un Webdriver.Chrome()
    '''

    # Extraire le HTML actuel et le parser avec BeautifulSoup
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
    # Pour les joueurs ayant arreté leur carrière, il est précisé en quelle année elle s'est terminée.
    # Comme ce n'est pas le cas sur la page du premier joueur, on rajoute à la main
    if len(labels)==7:
        labels.append("Dernière saison")

    return labels


# Récupération des liens vers les pages des joueurs

def Scrap_url_page(driver):

    '''
    Renvoie une liste contenant les urls des pages de joueurs disponibles depuis la page visitée.
    La liste d'url servira à récupérer les données des joueurs.
    Paramètres :
        - driver : Un Webdriver selenium. On utilisera toujours un Webdriver.Chrome()
    '''

    # Extraire le HTML actuel et le parser avec BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Scrapping de la liste des url
    liste_joueurs_brute = soup.find_all('div',{'class':'name'})
    liste_joueurs = [joueur.find('a') for joueur in liste_joueurs_brute]
    liste_url = [joueur['href'] for joueur in liste_joueurs]

    return liste_url


# Cliquer sur le bouton amenant sur une page de joueur donnée

def page_joueur(driver,url):

    '''
    Clique sur l'élément qui renvoie vers la page dont l'url est passé en argument.
    Cette fonction va permettre d'aller sur les pages des joueurs dont on souhaite récupérer les données.

    Paramètres :
        - driver : Un Webdriver selenium. On utilisera toujours un Webdriver.Chrome()
        - url : Une chaine de caractère de la forme "https://www.lnh.fr/liquimoly-starligue/joueurs/prenom-nom". Page du joueur dont on souhaite récupérer les données.
    '''

    # On cherche le lien qui nous amène à la page du joueur depuis la page des stats de match
    element = driver.find_element('xpath',f"//a[@href='{url}']")

    # On scrolle jusqu'à l'élément pour pas avoir de pb durant la visite de la page 
    position_clique = driver.execute_script("return arguments[0].offsetTop;", element)
    driver.execute_script(f"window.scrollTo(0, {position_clique});")

    # On clique sur le lien   
    element.click()


# Scrapping des données de tout les joueurs d'une page du tableau

def Scrap_tableau_joueur(driver,dictionnaire,liste_labels):

    '''
    Remplit un dictionnaire avec les données des pages des joueurs accessibles depuis la page visitée.
    Remplit également une liste avec le nom des colonnes du tableau de la page d'un joueur.
    Cette fonction se base sur les fonctions 'Scrap_page_joueur', 'entete_infos_joueur', 'Scrap_url_page' et 'page_joueur'.

    Paramètres :
        - driver : Un Webdriver selenium. On utilisera toujours un Webdriver.Chrome()
        - dictionnaire : Un dictionnaire python. Il sera rempli avec les données de la page visitée afin de créer un DataFrame.
        - liste_labels : Une liste python. Elle sera remplie avec le nom des colonnes du tableau de la page d'un joueur.   
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





