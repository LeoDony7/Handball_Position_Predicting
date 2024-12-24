import pandas as pd
# # Afficher les premières lignes des deux DataFrames pour visualiser les données
print("Aperçu du fichier 'donnees_match' :")
print(donnees_match.head())
print("\nAperçu du fichier 'donnees_physique' :")
print(donnees_physique.head())

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

# print(donnees_combinees.head())

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
