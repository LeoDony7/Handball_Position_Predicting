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
    if 'Nom formate' in dataframe2.columns:
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

