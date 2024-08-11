# Gestionnaire de Suivi des Demandes de Recherche d'Emploi

## Description
Ce projet est une application Python permettant de suivre les demandes de recherche d'emploi, d'immersion, et de stage. L'application utilise une interface graphique développée avec Tkinter, une base de données SQLite pour stocker les informations des demandes, et permet d'exporter les données vers un fichier Excel.

## Fonctionnalités
- **Ajouter une demande :** Ajoutez une nouvelle demande de recherche d'emploi, d'immersion, ou de stage avec les détails de l'entreprise, du poste, et des coordonnées.
- **Afficher les demandes :** Visualisez toutes les demandes stockées dans la base de données. Utilisez des filtres pour rechercher par entreprise, date, type de demande, ou statut.
- **Mettre à jour le statut :** Mettez à jour le statut d'une demande (en attente, relance, acceptée, refusée).
- **Relancer une demande :** Relancez une demande en mettant à jour la date de dernière relance.
- **Supprimer une demande :** Supprimez une demande sélectionnée de la base de données.
- **Vérifier les rappels :** Recevez des notifications de rappel pour les demandes en attente depuis au moins 7 jours.
- **Exporter les données :** Exportez les données de la base de données vers un fichier Excel.
- **Recherche et filtrage :** Filtrez les demandes par entreprise, date, type de demande, ou statut.

## Prérequis
Assurez-vous d'avoir Python 3.x installé sur votre système.

Vous aurez également besoin des modules Python suivants :
- `tkinter`
- `sqlite3`
- `plyer`
- `pandas`
- `openpyxl`
  
Ces modules peuvent être installés avec la commande suivante :
```bash
pip install tkinter plyer pandas openpyxl

Installation
Clonez ou téléchargez ce dépôt sur votre machine locale.
Assurez-vous que le script suivi_demandes_recherche_emploi.py est dans un répertoire dédié.
Les chemins des fichiers SQLite et Excel sont automatiquement configurés pour être relatifs au répertoire contenant le script.

Utilisation
Exécutez le script suivi_demandes_recherche_emploi.py.
L'interface utilisateur s'ouvre avec plusieurs options pour gérer vos demandes.
Ajoutez une nouvelle demande en entrant les informations nécessaires et cliquez sur "Ajouter Demande".
Filtrez et recherchez des demandes existantes en utilisant les champs de recherche.
Mettez à jour le statut des demandes, relancez-les, ou supprimez-les en utilisant les boutons appropriés.
Exportez vos données vers un fichier Excel en cliquant sur "Exporter".
Recevez des notifications de rappel pour les demandes en attente toutes les heures.

Structure du Projet
diff
Copier le code
- suivi_demandes_recherche_emploi.py : Le script principal qui contient toute la logique de l'application.
- suivi_demandes_recherche_emploi.db : La base de données SQLite contenant les informations sur les demandes.
- demandes_recherche_emploi.xlsx : Le fichier Excel généré pour l'exportation des données.

Notes
Les dates doivent être saisies au format JJ-MM-AAAA.
L'application envoie des notifications de rappel pour les demandes relancee en attente depuis au moins 7 jours.
Les statuts "Accepté" et "Refusé" bloquent toute nouvelle relance.

Licence
Ce projet est libre de droit. Vous pouvez l'utiliser, le modifier, et le distribuer comme vous le souhaitez.

Auteur
Développé par complexboy.