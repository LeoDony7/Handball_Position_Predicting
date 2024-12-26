## Traitement et Nettoyage du DataFrame contenant les données de matchs

import pandas as pd
from Fonctions_scrapping import telechargement_DF


# Fonction qui normalise le nom d'un joueur

def normalisation(nom_joueur):

    '''
    Cette fonction permet de normaliser l'écriture du nom d'un joueur, passant de NOM Prénom à Prénom Nom.
    '''

    mots = nom_joueur.split()

    if len(mots)==2:
        return ' '.join([mots[1].capitalize(),mots[0].capitalize()])
    elif len(mots) >=3 :
        nom=[]
        prenom= []
        for mot in mots:
            if mot.isupper():
                nom.append(mot.capitalize())
            else:
                prenom.append(mot.capitalize())
        return ' '.join(prenom+nom)
    else :
        return nom_joueur


# Fonction qui applique le formatage à un DataFrame

def nom_formate(dataframe):

    '''
    Cette fonction permet d'ajouter au DataFrame une colonne avec les noms au format Prénom Nom.
    '''

    dataframe['Nom formate'] = dataframe.index.map(normalisation)


## Fonction qui met les données du tableau dans le bon format

def traitement_pourcentages(dataframe):

    '''
    Cette fonction permet de nettoyer les données du DataFrame sur les matchs.
    Certaines colonnes ont des valeurs de la 'forme nombre tirs réussis / nombres tirs tentés'.
    On souhaite alors remplacer de telles colonnes par deux colonnes, contenant les valeurs numériques associées.
    La fonction modifie seulement le DataFrame, elle ne renvoie rien.
    '''

    # Colonnes à traiter et leurs nouveaux noms
    colonnes_a_traiter = {'totalbuts': ['Total buts', 'Total tirs'],
                          'butstirs': ['Buts dans le jeu', 'Tirs dans le jeu'],
                          'butspenalty': ['Penalty réussis', 'Tirs de Penalty']
                          }

    # Traiter chaque colonne spécifiée
    for col, nouveaux_noms in colonnes_a_traiter.items():
        if col in dataframe.columns:
            # Trouver l'index de la colonne actuelle
            col_index = dataframe.columns.get_loc(col)
        
            # Spliter la colonne en deux et créer les nouvelles colonnes
            nouvelles_valeurs = dataframe[col].str.split(" / ", expand=True)
        
            # Vérifier si les nouvelles colonnes existent déjà
            for i, nouveau_nom in enumerate(nouveaux_noms):
                if nouveau_nom in dataframe.columns:
                    # Supprimer les colonnes existantes avant d'en insérer de nouvelles
                    dataframe.drop(columns=[nouveau_nom], inplace=True)
            
                # Ajouter la colonne avec les nouvelles valeurs
                dataframe.insert(col_index + i, nouveau_nom, pd.to_numeric(nouvelles_valeurs[i], errors='coerce'))


# Fonction qui gère toutes les étapes de traitement d'un coup

def traitement(dataframe,nom_fichier= None):

    '''
    Cette fonction réalise toutes les étapes du traitement du DataFrame des données de matchs.
    '''

    nom_formate(dataframe)
    traitement_pourcentages(dataframe)

    if nom_fichier:
        telechargement_DF(dataframe,nom_fichier)

    else:
        return dataframe


# Fonction qui permet de faire la jointure entre 2 DataFrames

def jointure_df(dataframe1,dataframe2,telechargement = None):

    '''
    Cette fonction permet d'effectuer la jointure entre nos 2 DataFrames.
    La jointure s'effectue sur le nom des joueurs, en utilisant le format Prénom Nom.
    '''
    if 'Nom formate' in dataframe2.columns:
        donnees_combinees = pd.merge(dataframe1,dataframe2,left_index= True, right_on='Nom formate', how='inner')
        donnees_combinees.set_index('Nom formate', inplace=True)

        if telechargement:
            telechargement_DF(donnees_combinees,telechargement)
        else:
            return donnees_combinees
    else:
        raise ValueError("La colonne 'Nom formate' n'appartient pas au DataFrame, jointure impossible")


## Version Léo

def normalisation(nom_joueur):

    '''
    Cette fonction permet de normaliser l'écriture du nom d'un joueur, passant de NOM Prénom à Prénom Nom.
    '''

    mots = nom_joueur.split()

    if len(mots)==2:
        return ' '.join([mots[1].capitalize(),mots[0].capitalize()])
    elif len(mots) >=3 :
        nom=[]
        prenom= []
        for mot in mots:
            if mot.isupper():
                nom.append(mot.capitalize())
            else:
                prenom.append(mot.capitalize())
        return ' '.join(prenom+nom)
    else :
        return nom_joueur
    

def nom_formate(dataframe):

    '''
    Cette fonction permet d'ajouter au DataFrame une colonne avec les noms au format Prénom Nom.
    '''

    dataframe['Nom formate'] = dataframe.index.map(normalisation)
    

def jointure_df(dataframe1,dataframe2,telechargement = None):

    '''
    Cette fonction permet d'effectuer la jointure entre nos 2 DataFrames.
    La jointure s'effectue sur le nom des joueurs, en utilisant le format Prénom Nom.
    '''
    if 'Nom formate' in dataframe2.columns():
        donnees_combinees = pd.merge(dataframe1,dataframe2,left_index= True, right_on='Nom formate', how='inner')
        donnees_combinees.set_index('Nom formate', inplace=True)

        if telechargement:
            telechargement_DF(donnees_combinees,telechargement)

        return donnees_combinees
    else:
        raise ValueError("La colonne 'Nom formate' n'appartient pas au DataFrame, jointure impossible")

def traitement_pourcentages(dataframe):

    '''
    Cette fonction permet de nettoyer les données du DataFrame sur les matchs.
    Certaines colonnes ont des valeurs de la 'forme nombre tirs réussis / nombres tirs tentés'.
    On souhaite alors remplacer de telles colonnes par deux colonnes, contenant les valeurs numériques associées.
    La fonction modifie seulement le DataFrame, elle ne renvoie rien.
    '''

    # Colonnes à traiter et leurs nouveaux noms
    colonnes_a_traiter = {'totalbuts': ['Total buts', 'Total tirs'],
                          'butstirs': ['Buts dans le jeu', 'Tirs dans le jeu'],
                          'butspenalty': ['Penalty réussis', 'Tirs de Penalty']
                          }

    # Traiter chaque colonne spécifiée
    for col, nouveaux_noms in colonnes_a_traiter.items():
        if col in dataframe.columns:
            # Trouver l'index de la colonne actuelle
            col_index = dataframe.columns.get_loc(col)
        
            # Spliter la colonne en deux et créer les nouvelles colonnes
            nouvelles_valeurs = dataframe[col].str.split(" / ", expand=True)
        
            # Vérifier si les nouvelles colonnes existent déjà
            for i, nouveau_nom in enumerate(nouveaux_noms):
                if nouveau_nom in dataframe.columns:
                    # Supprimer les colonnes existantes avant d'en insérer de nouvelles
                    dataframe.drop(columns=[nouveau_nom], inplace=True)
            
                # Ajouter la colonne avec les nouvelles valeurs
                dataframe.insert(col_index + i, nouveau_nom, pd.to_numeric(nouvelles_valeurs[i], errors='coerce'))


## Version Cyrille 
'''
# Fonctions pour normaliser les noms de manière cohérente (inverser Prénom Nom en NOM PRENOM)
def normaliser_nom(nom):
    # Séparer le nom et le prénom
    parties = nom.split()
    if len(parties) >1 :
        # Par défaut, on considère que le prénom n'est composé que d'un seul mot qui est le premier
        return f"{' '.join(parties[1:]).upper()} {parties[0].upper()}"
    return nom  # Si le format n'est pas correct, on laisse tel quel

# Fonction pour traiter les cas particuliers (prénoms+noms en trois mots dont deux pour le prénom) 
def normaliser_prenom_deux_mots(nom):
    parties = nom.split()
    if len(parties) > 2:  # On vérifie qu'il y a au moins trois mots
        # Les deux premiers mots forment le prénom
        prenom = ' '.join(parties[:2])
        nom_famille = ' '.join(parties[2:])
        return f"{nom_famille.upper()} {prenom.upper()}"
    return nom

# Appliquer la première fonction aux index de donnees_physique
donnees_physique['NOM PRENOM'] = donnees_physique.index.map(normaliser_nom)

# Appliquer la deuxième fonction de normalisation sur les lignes non fusionnées
lignes_non_traitees_donnees_physique = donnees_physique[~donnees_physique['NOM PRENOM'].isin(donnees_combinees.index)].copy()
lignes_non_traitees_donnees_physique['NOM PRENOM'] = lignes_non_traitees_donnees_physique.index.to_series().map(normaliser_prenom_deux_mots)

# Copier les lignes non fusionnées normalisées dans 'donnees_physique'
donnees_physique.update(lignes_non_traitees_donnees_physique)

# Créer une nouvelle colonne de noms normalisés dans donnees_match pour mettre tout en majuscules
donnees_match['NOM PRENOM'] = donnees_match.index.str.upper()

# Afficher les noms normalisés
print("\nIndex normalisés dans 'donnees_match' :")
print(donnees_match['NOM PRENOM'].head())

print("\nIndex normalisés dans 'donnees_physique' :")
print(donnees_physique['NOM PRENOM'].head())

# Fusionner les deux DataFrames en utilisant les noms normalisés comme index final
donnees_combinees = pd.merge(donnees_match, donnees_physique, on='NOM PRENOM', how='inner')
donnees_combinees.set_index('NOM PRENOM', inplace=True)

# Vérifier le nombre total de lignes après fusion
print("\nNombre total de lignes dans le DataFrame fusionné :", len(donnees_combinees))

# Lignes qui ne se sont pas fusionnées dans les DataFrames normalisés
lignes_non_fusionnees_match_normalise = donnees_match[~donnees_match['NOM PRENOM'].isin(donnees_combinees.index)]


############### TRAITEMENT DU NOUVEAU DATAFRAME ############
# Colonnes à traiter et leurs nouveaux noms
colonnes_a_traiter = {
    'totalbuts': ['Total buts', 'Total tirs'],
    'butstirs': ['Buts dans le jeu', 'Tirs dans le jeu'],
    'butspenalty': ['Penalty réussis', 'Tirs de Penalty']
}

# Copier le DataFrame pour préserver les données originales
data = donnees_combinees

# Traiter chaque colonne spécifiée
for col, nouveaux_noms in colonnes_a_traiter.items():
    if col in data.columns:
        # Trouver l'index de la colonne actuelle
        col_index = data.columns.get_loc(col)
        
        # Spliter la colonne en deux et créer les nouvelles colonnes
        nouvelles_valeurs = data[col].str.split(" / ", expand=True)
        
        # Vérifier si les nouvelles colonnes existent déjà
        for i, nouveau_nom in enumerate(nouveaux_noms):
            if nouveau_nom in data.columns:
                # Supprimer les colonnes existantes avant d'en insérer de nouvelles
                data.drop(columns=[nouveau_nom], inplace=True)
            
            # Ajouter la colonne avec les nouvelles valeurs
            data.insert(col_index + i, nouveau_nom, pd.to_numeric(nouvelles_valeurs[i], errors='coerce'))
        
        # Supprimer la colonne originale
        data.drop(columns=[col], inplace=True)

# Afficher les premières lignes du DataFrame modifié
data

'''