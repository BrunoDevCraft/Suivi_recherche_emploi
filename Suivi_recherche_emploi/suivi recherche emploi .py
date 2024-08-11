import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
from plyer import notification
import pandas as pd
from openpyxl import load_workbook
import os

# Déterminer le répertoire où se trouve le script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Créer des chemins absolus pour les fichiers
db_path = os.path.join(script_dir, 'suivi_demandes_recherche_emploi.db')
excel_path = os.path.join(script_dir, 'demandes_recherche_emploi.xlsx')

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

# Fonction pour ajouter une nouvelle demande
def ajouter_demande():
    type_demande = var_type_demande.get()
    entreprise = entry_entreprise.get()
    poste = entry_poste.get()
    date_initiale = entry_date_initiale.get()
    coordonnees = entry_coordonnees.get()

    # Validation de la date
    try:
        date_demande = datetime.strptime(date_initiale, "%d-%m-%Y").date()
    except ValueError:
        messagebox.showerror("Erreur de format", "Veuillez entrer la date au format JJ-MM-AAAA")
        return

    statut = "En attente"
    
    cursor.execute('''INSERT INTO demandes (type_demande, entreprise, poste, coordonnees, date_demande, statut) 
                      VALUES (?, ?, ?, ?, ?, ?)''', (type_demande, entreprise, poste, coordonnees, date_demande, statut))
    conn.commit()
    afficher_demandes()

# Fonction pour afficher les demandes
def afficher_demandes():
    cursor.execute('SELECT * FROM demandes')
    rows = cursor.fetchall()
    listbox.delete(*listbox.get_children())
    for row in rows:
        id_demande, type_demande, entreprise, poste, date_demande, statut, date_derniere_relance, coordonnees = row
        date_formatee = datetime.strptime(date_demande, "%Y-%m-%d").strftime("%d-%m-%Y")
        relance_formatee = datetime.strptime(date_derniere_relance, "%Y-%m-%d").strftime("%d-%m-%Y") if date_derniere_relance else "N/A"
        listbox.insert("", "end", values=(id_demande, type_demande, entreprise, poste, coordonnees, date_formatee, statut, relance_formatee))

# Fonction pour afficher les demandes
def afficher_demandes():
    recherche_entreprise = entry_recherche.get()
    recherche_date = entry_recherche_date.get()
    recherche_type = var_recherche_type.get()
    recherche_statut = var_recherche_statut.get()

    # Construire la requête SQL avec les filtres
    query = "SELECT * FROM demandes WHERE 1=1"
    params = []

    if recherche_entreprise:
        query += " AND entreprise LIKE ?"
        params.append(f"%{recherche_entreprise}%")
    
    if recherche_date:
        try:
            recherche_date = datetime.strptime(recherche_date, "%d-%m-%Y").date()
            query += " AND date_demande = ?"
            params.append(recherche_date)
        except ValueError:
            messagebox.showerror("Erreur de format", "Veuillez entrer la date au format JJ-MM-AAAA")
            return
    
    if recherche_type and recherche_type != " ":
        query += " AND type_demande = ?"
        params.append(recherche_type)

    if recherche_statut and recherche_statut != "":
        query += " AND statut = ?"
        params.append(recherche_statut)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    listbox.delete(*listbox.get_children())
    for row in rows:
        id_demande, type_demande, entreprise, poste, date_demande, statut, date_derniere_relance, coordonnees = row
        date_formatee = datetime.strptime(date_demande, "%Y-%m-%d").strftime("%d-%m-%Y")
        relance_formatee = datetime.strptime(date_derniere_relance, "%Y-%m-%d").strftime("%d-%m-%Y") if date_derniere_relance else "N/A"
        listbox.insert("", "end", values=(id_demande, type_demande, entreprise, poste, coordonnees, date_formatee, statut, relance_formatee))




# Fonction pour gérer les rappels
def verifier_rappels():
    today = datetime.now().date()
    cursor.execute('SELECT id, entreprise, poste, date_derniere_relance, statut FROM demandes WHERE statut="En attente"')
    rows = cursor.fetchall()
    
    for row in rows:
        id_demande, entreprise, poste, date_derniere_relance, statut = row
        if date_derniere_relance:
            date_relance = datetime.strptime(date_derniere_relance, "%Y-%m-%d").date()
        else:
            continue  # S'il n'y a pas de date de relance, ne pas faire de rappel

        # Vérifier si la dernière relance est d'au moins 7 jours
        if today >= (date_relance + timedelta(days=7)):
            notification.notify(
                title="Rappel de relance",
                message=f"Pensez à relancer votre demande pour le poste {poste} chez {entreprise}.",
                timeout=10
            )

# Fonction pour mettre à jour le statut
def mettre_a_jour_statut(nouveau_statut):
    try:
        selection = listbox.selection()
        if not selection:
            return  # Si aucune sélection, ne rien faire

        item = listbox.item(selection[0])
        demande_id = item['values'][0]
        statut_actuel = item['values'][6]  # Récupère le statut actuel

        # Empêcher la relance si le statut est "Accepté" ou "Refusé"
        if statut_actuel in ["Accepté", "Refusé"]:
            messagebox.showwarning("Action non autorisée", "Vous ne pouvez pas relancer une demande acceptée ou refusée.")
            return

        date_aujourd_hui = datetime.now().date()

        # Mettre à jour le statut et la date de dernière relance
        if nouveau_statut == "Relance":
            cursor.execute('UPDATE demandes SET statut = ?, date_derniere_relance = ? WHERE id = ?', 
                           (nouveau_statut, date_aujourd_hui, demande_id))
        else:
            cursor.execute('UPDATE demandes SET statut = ? WHERE id = ?', 
                           (nouveau_statut, demande_id))

        conn.commit()
        afficher_demandes()
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue lors de la mise à jour du statut : {e}")

# Fonction pour supprimer une demande
def supprimer_demande():
    try:
        selection = listbox.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une demande à supprimer.")
            return

        item = listbox.item(selection[0])
        demande_id = item['values'][0]

        cursor.execute('DELETE FROM demandes WHERE id = ?', (demande_id,))
        conn.commit()
        afficher_demandes()
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue lors de la suppression : {e}")

# Fonction pour exporter les données au format Excel
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

# Fonction pour vérifier les rappels automatiquement
def verifier_rappels_periodiquement():
    verifier_rappels()
    root.after(3600000, verifier_rappels_periodiquement)  # Vérifie toutes les heures

# Fonction pour réinitialiser les filtres et afficher toutes les demandes
def reset_filtres():
    entry_recherche.delete(0, tk.END)
    entry_recherche_date.delete(0, tk.END)
    var_recherche_type.set(options[0])
    var_recherche_statut.set(statut_options[0])
    afficher_demandes()


# Interface utilisateur avec Tkinter et ttk
root = tk.Tk()
root.title("Suivi des Demandes")
root.geometry("1270x500")

# Style ttk
style = ttk.Style()
style.theme_use("clam")

# Ajouter les Frames pour l'organisation des éléments
frame_form = ttk.LabelFrame(root, text="Demande")
frame_form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

frame_actions = ttk.LabelFrame(root, text="Action")
frame_actions.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

frame_listbox = ttk.LabelFrame(root, text="Liste suivie Demandes")
frame_listbox.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

# Créer une Frame pour contenir le label et l'option menu pour "Type de demande"
frame_type = ttk.Frame(frame_form)
frame_type.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Placer le label et l'option menu côte à côte dans cette Frame
label_type = ttk.Label(frame_type, text="Type de demande:")
label_type.pack(side="left", padx=5, pady=5)

options = [" ", "Immersion", "Stage", "Recherche Emploi"]
var_type_demande = tk.StringVar(root)
var_type_demande.set(options[0])
option_menu = ttk.OptionMenu(frame_type, var_type_demande, *options)
option_menu.pack(side="left", padx=5, pady=5, fill="x", expand=True)

# Créer une Frame pour contenir le label et l'entry
frame_entreprise = ttk.Frame(frame_form)
frame_entreprise.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Placer le label et l'entry côte à côte dans cette Frame
label_entreprise = ttk.Label(frame_entreprise, text="Entreprise:")
label_entreprise.pack(side="left", padx=5, pady=5)

entry_entreprise = ttk.Entry(frame_entreprise)
entry_entreprise.pack(side="left", padx=5, pady=5, fill="x", expand=True)

# Créer une Frame pour contenir le label et l'entry pour "Poste"
frame_poste = ttk.Frame(frame_form)
frame_poste.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

# Placer le label et l'entry côte à côte dans cette Frame
label_poste = ttk.Label(frame_poste, text="Poste:")
label_poste.pack(side="left", padx=5, pady=5)

entry_poste = ttk.Entry(frame_poste)
entry_poste.pack(side="left", padx=5, pady=5, fill="x", expand=True)

# Créer une Frame pour contenir le label et l'entry pour "Date initiale"
frame_date_initiale = ttk.Frame(frame_form)
frame_date_initiale.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

# Placer le label et l'entry côte à côte dans cette Frame
label_date_initiale = ttk.Label(frame_date_initiale, text="Date(JJ-MM-AAAA):")
label_date_initiale.pack(side="left", padx=5, pady=5)

entry_date_initiale = ttk.Entry(frame_date_initiale)
entry_date_initiale.pack(side="left", padx=5, pady=5, fill="x", expand=True)

# Créer une Frame pour contenir le label et l'entry pour "Coordonnées"
frame_coordonnees = ttk.Frame(frame_form)
frame_coordonnees.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

# Placer le label et l'entry côte à côte dans cette Frame
label_coordonnees = ttk.Label(frame_coordonnees, text="Coordonnées:")
label_coordonnees.pack(side="left", padx=5, pady=5)

entry_coordonnees = ttk.Entry(frame_coordonnees)
entry_coordonnees.pack(side="left", padx=5, pady=5, fill="x", expand=True)

button_ajouter = ttk.Button(frame_form, text="Ajouter Demande", command=ajouter_demande)
button_ajouter.grid(row=0, column=5, padx=5, pady=5)

# Créer une Frame pour contenir le label et l'entry pour la recherche
frame_recherche = ttk.Frame(frame_form)
frame_recherche.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Placer le label et l'entry côte à côte dans cette Frame
label_recherche = ttk.Label(frame_recherche, text="par entreprise:")
label_recherche.pack(side="left", padx=5, pady=5)

entry_recherche = ttk.Entry(frame_recherche)
entry_recherche.pack(side="left", padx=5, pady=5, fill="x", expand=True)

# Créer une Frame pour contenir le label et l'entry pour la recherche par date
frame_recherche_date = ttk.Frame(frame_form)
frame_recherche_date.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

# Placer le label et l'entry côte à côte dans cette Frame
label_recherche_date = ttk.Label(frame_recherche_date, text="par date:")
label_recherche_date.pack(side="left", padx=5, pady=5)

entry_recherche_date = ttk.Entry(frame_recherche_date)
entry_recherche_date.pack(side="left", padx=5, pady=5, fill="x", expand=True)

# Créer une Frame pour contenir le label et l'option menu pour la recherche par type
frame_recherche_type = ttk.Frame(frame_form)
frame_recherche_type.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Placer le label et l'option menu côte à côte dans cette Frame
label_recherche_type = ttk.Label(frame_recherche_type, text="Recherche par type:")
label_recherche_type.pack(side="left", padx=5, pady=5)

options = [" ", "Immersion", "Stage", "Recherche Emploi"]
var_recherche_type = tk.StringVar(root)
var_recherche_type.set(options[0])
option_recherche_type = ttk.OptionMenu(frame_recherche_type, var_recherche_type, *options)
option_recherche_type.pack(side="left", padx=5, pady=5, fill="x", expand=True)

# Créer une Frame pour contenir le label et l'option menu pour le filtre par statut
frame_recherche_statut = ttk.Frame(frame_form)
frame_recherche_statut.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

# Placer le label et l'option menu côte à côte dans cette Frame
label_recherche_statut = ttk.Label(frame_recherche_statut, text="Filtrer par statut:")
label_recherche_statut.pack(side="left", padx=5, pady=5)

statut_options = ["", "En attente", "Relance", "Accepté", "Refusé"]
var_recherche_statut = tk.StringVar(root)
var_recherche_statut.set(statut_options[0])
option_recherche_statut = ttk.OptionMenu(frame_recherche_statut, var_recherche_statut, *statut_options)
option_recherche_statut.pack(side="left", padx=5, pady=5, fill="x", expand=True)

# Bouton pour déclencher la recherche
button_rechercher = ttk.Button(frame_form, text="Rechercher", command=afficher_demandes)
button_rechercher.grid(row=1, column=4, padx=5, pady=5, sticky="w")

# Bouton pour réinitialiser les filtres
button_reset = ttk.Button(frame_form, text="Réinitialiser", command=reset_filtres)
button_reset.grid(row=1, column=4, padx=5, pady=5, sticky="e")

# Listbox avec ttk.Treeview pour des colonnes séparées
listbox = ttk.Treeview(frame_listbox, columns=("ID", "Type", "Entreprise", "Poste", "Coordonnées", "Date Demande", "Statut", "Relance"), show="headings")
listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Définir les titres des colonnes
for col in listbox["columns"]:
    listbox.heading(col, text=col)
    listbox.column(col, width=100)

# Scrollbar pour la listbox
scrollbar = ttk.Scrollbar(frame_listbox, orient="vertical", command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")

# Boutons d'action
button_relance = ttk.Button(frame_actions, text="Relancer", command=lambda: mettre_a_jour_statut("Relance"))
button_relance.grid(row=0, column=0, padx=5, pady=5)

button_accepter = ttk.Button(frame_actions, text="Accepter", command=lambda: mettre_a_jour_statut("Accepté"))
button_accepter.grid(row=0, column=1, padx=5, pady=5)

button_refuser = ttk.Button(frame_actions, text="Refuser", command=lambda: mettre_a_jour_statut("Refusé"))
button_refuser.grid(row=0, column=2, padx=5, pady=5)

button_rappels = ttk.Button(frame_actions, text="Vérifier Rappels", command=verifier_rappels)
button_rappels.grid(row=0, column=3, padx=5, pady=5)

button_supprimer = ttk.Button(frame_actions, text="Supprimer", command=supprimer_demande)
button_supprimer.grid(row=0, column=4, padx=5, pady=5)

button_exporter = ttk.Button(frame_actions, text="Exporter", command=exporter_excel)
button_exporter.grid(row=0, column=5, padx=5, pady=5)

# Démarrer la vérification automatique des rappels
verifier_rappels_periodiquement()

afficher_demandes()

root.mainloop()
