import sqlite3
import os

# Déterminer le répertoire où se trouve le script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Créer des chemins absolus pour les fichiers
db_path = os.path.join(script_dir, 'suivi_demandes_recherche_emploi.db')

# Connexion à la base de données SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Création de la table si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS demandes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type_demande TEXT,
                    entreprise TEXT,
                    poste TEXT,
                    date_demande DATE,
                    statut TEXT,
                    date_derniere_relance DATE,
                    coordonnees TEXT
                )''')
conn.commit()