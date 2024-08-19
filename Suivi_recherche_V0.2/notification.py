import tkinter as tk
from tkinter import ttk, messagebox
from plyer import notification
from datetime import datetime, timedelta
import time
from db import conn, cursor
import os

# Déterminer le répertoire où se trouve le script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize the Tkinter application
#root = tk.Tk()

# Fonction pour gérer les rappels
def verifier_rappels():
    today = datetime.now().date()
    cursor.execute('SELECT id, entreprise, poste, date_demande, date_derniere_relance, statut FROM demandes WHERE statut="En attente"')
    rows = cursor.fetchall()
    
    for row in rows:
        id_demande, entreprise, poste, date_demande, date_derniere_relance, statut = row
        date_demande = datetime.strptime(date_demande, "%Y-%m-%d").date()
        
        # Vérifier si la date de demande est passée depuis 7 jours
        if today >= (date_demande + timedelta(days=7)):
            notification.notify(
                title="Rappel de relance",
                message=f"Pensez à relancer votre demande pour le poste {poste} chez {entreprise}. (Date de demande : {date_demande.strftime('%d-%m-%Y')})",
                timeout=10
            )

        # Vérifier si la dernière relance est d'au moins 7 jours
        if date_derniere_relance:
            date_relance = datetime.strptime(date_derniere_relance, "%Y-%m-%d").date()
            if today >= (date_relance + timedelta(days=7)):
                notification.notify(
                    title="Rappel de relance",
                    message=f"Pensez à relancer votre demande pour le poste {poste} chez {entreprise}. (Dernière relance : {date_relance.strftime('%d-%m-%Y')})",
                    timeout=10
                )

# Fonction pour vérifier les rappels automatiquement
#def verifier_rappels_periodiquement():
#    while True:
#        verifier_rappels()
        #after(3600000, verifier_rappels_periodiquement)  # Vérifie toutes les heures
#        time.sleep(3600)  # Vérifie toutes les heures
    
    
# Démarrer la vérification automatique des rappels
#verifier_rappels_periodiquement()

# Start the Tkinter main loop
#root.mainloop()
