CREATE TABLE demandes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_demande TEXT,
    entreprise TEXT,
    poste TEXT,
    coordonnees TEXT,
    date_demande DATE,
    statut TEXT,
    date_derniere_relance DATE
);
