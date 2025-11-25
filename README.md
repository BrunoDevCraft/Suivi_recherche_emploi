
## 📄 `README.md`

# 💼 Suivi des Demandes d'Emploi

[](https://www.google.com/search?q=LICENSE.txt)
[](https://www.google.com/search?q=package.json)

> Une application de bureau moderne et légère, conçue avec Electron, pour gérer et suivre l'état de vos candidatures d'emploi, de la relance à l'acceptation. Ne perdez plus jamais une opportunité de vue \!

## ✨ Fonctionnalités Clés

Ce gestionnaire a été développé pour offrir une expérience fluide et centralisée :

  * **💻 Application Desktop Multiplateforme :** Basé sur **Electron**, fonctionne sur Windows, macOS et Linux (configuré pour Windows dans `package.json`).
  * **💾 Base de Données Locale :** Utilise **`better-sqlite3`** pour un stockage des données rapide, fiable et 100% local (`db/db_manager.js` et non fourni).
  * **📊 Suivi des Statuts :** Gère les statuts de candidature (Envoyé, Relance, Accepté, Refusé) avec mise à jour facile.
  * **🔔 Système de Rappel :** Utilise **`node-notifier`** pour les rappels de relance (géré dans `main.js`).
  * **📤 Exportation Excel :** Exportez toutes vos données de suivi vers un fichier Excel (`demandes_recherche_emploi.xlsx`) en utilisant **`exceljs`**.

-----

## 🛠️ Technologies Utilisées

| Technologie | Rôle |
| :--- | :--- |
| **Electron 28+** | Framework pour le développement d'applications de bureau. |
| **Node.js** | Environnement d'exécution JavaScript pour la logique du processus principal (`main.js`). |
| **SQLite3** | Base de données embarquée pour le stockage local des données. |
| **HTML / CSS / JS** | Structure de l'interface utilisateur (`index.html`, `renderer.js`, `style.css`). |
| **Electron Builder** | Packaging et distribution des exécutables (EXE). |

-----

## 🚀 Installation et Démarrage

Télécharger le fichier : "SuiviDemandesEmploi Setup 1.0.0.exe"
1 - lancer
2 - installer
3 - c'est près!!
-----

## 🤝 Contribution

Si vous trouvez un bug ou avez une suggestion d'amélioration :

1.  Faites un `fork` du projet.
2.  Créez une nouvelle branche (`git checkout -b feature/amelioration`).
3.  Commitez vos changements (`git commit -m 'Ajout d'une fonctionnalité X'`).
4.  Poussez vers la branche (`git push origin feature/amelioration`).
5.  Ouvrez une **Pull Request**.

-----

## 📄 Licence

Ce projet est distribué sous la licence MIT. Voir le fichier [`LICENSE.txt`](https://www.google.com/search?q=LICENSE.txt) pour plus d'informations.

**© 2025 BrunoDevCraft**
