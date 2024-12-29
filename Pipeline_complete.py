from Scrapping_donnees_fonction import *

# /!\ Modifier le nom des fichiers quand on aura déplacé les fonctions
# et ne pas tout importer, seulement les trucs utiles
from Handball_Position_Predicting.Brouillons.Stats_descriptives import *

from Choix_modele import *
from Evaluation import *
from Prediction import *

Scrapping(nom_df_match="DF_match_rapport.csv",nom_df_physique="DF_joueur_rapport.csv")

DF_match_rapport = pd.read_csv("DF_match_rapport.csv",index_col=0)
DF_joueur_rapport = pd.read_csv("DF_joueur_rapport.csv",index_col=0)

DF_joueur_rapport_nettoye = cleaning(DF_joueur_rapport)

parametre_KNN(DF_joueur_rapport_nettoye)
parametres_SVM(DF_joueur_rapport_nettoye)
parametres_Random_Forest(DF_joueur_rapport_nettoye)

## -> on en déduit les best paramètres pour chaque modèle

Eval_modele_KNN(DF_joueur_rapport_nettoye,best_k)
Eval_modele_SVM(DF_joueur_rapport_nettoye,best_parametres_SVM)
Eval_modele_Random_Forest(DF_joueur_rapport_nettoye,best_parametres_RF)

Prediction(DF_joueur_rapport_nettoye,"DF_joueur_prediction.csv")

DF_joueur_prediction = pd.read_csv("DF_joueur_prediction.csv",index_col=0)

## Ajouter la partie où on compare les performances

