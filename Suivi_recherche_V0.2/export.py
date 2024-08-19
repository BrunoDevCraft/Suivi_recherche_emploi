from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
from openpyxl import load_workbook
from db import cursor
import os

# Déterminer le répertoire où se trouve le script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Créer des chemins absolus pour les fichiers
excel_path = os.path.join(script_dir, 'demandes_recherche_emploi.xlsx')

def exporter_excel():
    try:
        cursor.execute('SELECT * FROM demandes')
        rows = cursor.fetchall()
        data = []
        for row in rows:
            id_demande, type_demande, entreprise, poste, date_demande, statut, date_derniere_relance, coordonnees = row
            date_formatee = datetime.strptime(date_demande, "%Y-%m-%d").strftime("%d-%m-%Y")
            relance_formatee = datetime.strptime(date_derniere_relance, "%Y-%m-%d").strftime("%d-%m-%Y") if date_derniere_relance else "N/A"
            data.append([id_demande, type_demande, entreprise, poste, coordonnees, date_formatee, statut, relance_formatee])

        df = pd.DataFrame(data, columns=["ID", "Type de demande", "Entreprise", "Poste", "Coordonnées", "Date demande", "Statut", "Date Dernière Relance"])
        df.to_excel(excel_path, index=False)

        wb = load_workbook(excel_path)
        ws = wb.active

        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column_letter].width = adjusted_width

        wb.save(excel_path)
        messagebox.showinfo("Exportation réussie", f"Les données ont été exportées vers '{excel_path}'.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'exportation : {e}")