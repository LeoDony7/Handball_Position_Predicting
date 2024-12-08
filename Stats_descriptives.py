import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Partie à adapter !!!
data = pd.read_csv("/Donnees_physique_joueurs.csv", index_col=0)

# Renommer les colonnes pour la compatibilité
noms_colonnes = ["Poste", "Nationalité", "Date de naissance",
                 "Âge", "Taille", "Poids", "Club actuel", "Dernière saison"]
data.columns = noms_colonnes

# Supprimer les unités et changer de type
data["Âge"] = data["Âge"].str.replace(r" ans", "", regex=True).astype(float)
data["Taille"] = data["Taille"].str.replace(r" cm", "", regex=True).astype(float)
data["Poids"] = data["Poids"].str.replace(r" kgs", "", regex=True).astype(float)

# Supprimer les 2 joueurs sur lesquels pas de données
data = data.dropna(subset=['Poste', 'Taille', 'Poids'])

# Création de tables différentes selon les postes
data_pivot = data[data['Poste'] == 'Pivot']
data_arriere = data[data['Poste'].isin(['Arrière Droit', 'Arrière Gauche'])]
data_centre = data[data['Poste'] == 'Demi Centre']
data_ailier = data[data['Poste'].isin(['Ailier Droit', 'Ailier Gauche'])]

# Initialiser le modèle de régression linéaire
model = LinearRegression()

# Fonction pour afficher les points et une droite de régression
def afficher_regression_et_points(dataset, color, label):

    X = dataset['Taille'].values.reshape(-1, 1)  # 2D requis pour LinearRegression
    y = dataset['Poids'].values

    model.fit(X, y)
    y_pred = model.predict(X)

    plt.scatter(dataset['Taille'], dataset['Poids'], color=color, label=label)
    plt.plot(dataset['Taille'], y_pred, color=color, linestyle='--', label=f"Régression ({label})")

# Créer le graphique
plt.figure(figsize=(10, 6))

# Ajouter les points et les droites pour chaque groupe
afficher_regression_et_points(data_pivot, 'red', 'Pivot')
afficher_regression_et_points(data_arriere, 'blue', 'Arrière')
afficher_regression_et_points(data_centre, 'green', 'Centre')
afficher_regression_et_points(data_ailier, 'orange', 'Ailier')

# Ajouter des labels et une légende
plt.xlabel("Taille (cm)")
plt.ylabel("Poids (kg)")
plt.title("Relation entre Taille et Poids selon le Poste avec régression")
plt.legend(loc="best", fontsize=10)
plt.grid(True)
plt.show()
