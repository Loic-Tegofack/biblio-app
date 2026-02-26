# 📚 Biblio - Application de Gestion de Bibliothèque

> Application moderne de gestion de bibliothèque développée en Python avec CustomTkinter et SQLite

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.0-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)
![Statut](https://img.shields.io/badge/Statut-En%20d%C3%A9veloppement-yellow.svg)

---

## 📖 Description

**Biblio** est une application complète de gestion de bibliothèque permettant de gérer efficacement un catalogue de livres, des auteurs, des utilisateurs et des emprunts. Conçue avec une interface moderne et intuitive grâce à CustomTkinter, elle offre une expérience utilisateur fluide et professionnelle.

### ✨ Points forts

- 🎨 **Interface moderne** : Design épuré avec CustomTkinter
- 🏗️ **Architecture MVC** : Code structuré et maintenable
- 🔒 **Gestion sécurisée** : Mots de passe hashés (SHA-256)
- 📊 **Gestion intelligente** : Validation automatique, gestion du stock, détection des retards
- 🔍 **Recherche avancée** : Filtrage et recherche multi-critères

---

## 🚀 Fonctionnalités

### ✅ Fonctionnalités implémentées

#### 📚 Gestion des Livres
- ✓ Ajout de livres avec gestion automatique des auteurs
- ✓ Modification des informations (titre, date, genre, état, stock)
- ✓ Suppression sécurisée avec confirmation
- ✓ Recherche par titre
- ✓ Affichage détaillé avec menu contextuel
- ✓ Gestion automatique du stock lors des emprunts/retours

#### ✍️ Gestion des Auteurs
- ✓ Ajout d'auteurs (nom, année de naissance, nationalité)
- ✓ Création automatique lors de l'ajout d'un livre
- ✓ Suppression (bloquée si l'auteur a des livres)
- ✓ Liste complète avec recherche

#### 👤 Gestion des Utilisateurs
- ✓ Création de comptes avec validation
- ✓ Mot de passe hashé (SHA-256)
- ✓ Suppression sécurisée
- ✓ Limitation à 3 emprunts simultanés par utilisateur

#### 📋 Gestion des Emprunts
- ✓ Affichage des emprunts en cours
- ✓ Détection automatique des retards (coloration rouge)
- ✓ Recherche d'emprunts par utilisateur
- ✓ Calcul automatique de la date de retour (+14 jours)
- ✓ Gestion automatique du stock (décrémentation/incrémentation)
- ✓ Blocage des emprunts si utilisateur en retard
- ✓ Affichage des détails utilisateur (quota d'emprunts)

### 🚧 En cours de développement

- ⏳ Menu contextuel pour valider les retours
- ⏳ Formulaire de création d'emprunt (admin)
- ⏳ Système de requêtes/réservations
- ⏳ Historique des emprunts par utilisateur
- ⏳ Statistiques et rapports
- ⏳ Authentification (admin/lecteur)
- ⏳ Interface lecteur avec fonctionnalités limitées

---

## 🛠️ Technologies utilisées

| Technologie | Version | Usage |
|-------------|---------|-------|
| **Python** | 3.10+ | Langage principal |
| **CustomTkinter** | 5.2.0 | Interface graphique moderne |
| **SQLite3** | 3.x | Base de données locale |
| **Hashlib** | stdlib | Hashage des mots de passe (SHA-256) |
| **Datetime** | stdlib | Gestion des dates d'emprunt |

---

## 📁 Structure du projet
```
biblio-app/
│
├── GUI_Biblio.py              # Interface graphique (Vue)
├── controleurBiblio.py        # Logique métier (Contrôleur)
├── script_sql_biblio.py       # Requêtes SQL (Modèle)
├── Biblio_model.py            # Gestion base de données
│
├── test02.db                  # Base de données SQLite (générée)
├── README.md                  # Documentation
└── .gitignore                 # Fichiers exclus de Git
```

---

## 📊 Schéma de la base de données
```sql
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   Auteur    │         │    Livre    │         │ Utilisateur  │
├─────────────┤         ├─────────────┤         ├──────────────┤
│ id          │◄────┐   │ id          │    ┌───►│ id           │
│ nom         │     └───│ auteur_id   │    │    │ nom          │
│ date_naiss. │         │ titre       │    │    │ prenom       │
│ nationalite │         │ date        │    │    │ adresse      │
└─────────────┘         │ genre       │    │    │ mdp (hash)   │
                        │ etat        │    │    └──────────────┘
                        │ nbre_exempl.│    │
                        └──────┬──────┘    │
                               │           │
                               │           │
                               ▼           ▼
                        ┌──────────────────────┐
                        │      Emprunt         │
                        ├──────────────────────┤
                        │ id                   │
                        │ livre_id (FK)        │
                        │ utilisateur_id (FK)  │
                        │ date_emprunt         │
                        │ date_retour_prevue   │
                        │ date_retour_effective│
                        └──────────────────────┘
```

---

## 🚀 Installation

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances
```bash
# Cloner le repository
git clone https://github.com/Loic-Tegofack/biblio-app.git
cd biblio-app

# Installer CustomTkinter
pip install customtkinter
```

---

## ▶️ Utilisation

### Lancer l'application
```bash
python GUI_Biblio.py
```

### Première utilisation

1. L'application crée automatiquement la base de données `test02.db`
2. Commencez par ajouter des auteurs et des livres
3. Créez des utilisateurs
4. Gérez les emprunts depuis l'onglet dédié

### Navigation

- **📚 Livres** : Gestion du catalogue
- **✍️ Auteurs** : Gestion des auteurs
- **👤 Utilisateurs** : Gestion des lecteurs
- **📋 Emprunts** : Gestion des emprunts et retours

---

## 🎯 Cas d'usage

### Ajouter un livre

1. Onglet **Livres** → Clic sur **"+ Nouveau livre"**
2. Remplir les champs obligatoires (Titre*, Auteur*, État*)
3. Si l'auteur n'existe pas, il sera créé automatiquement
4. Valider

### Rechercher un livre

1. Entrer le titre dans la barre de recherche
2. Cliquer sur **"Rechercher"**
3. Cliquer sur **"Afficher tout"** pour revenir à la liste complète

### Consulter les emprunts en retard

1. Onglet **Emprunts**
2. Cliquer sur **"⚠️ Livres en retard"**
3. Les emprunts en retard s'affichent avec coloration rouge

---

## 🔧 Configuration

### Paramètres modifiables

**Dans `controleurBiblio.py`, classe `Borrow_Manager`** :
```python
# Durée d'emprunt (ligne ~280)
date_retour_prevue = date_emprunt + timedelta(days=14)  # Modifier ici

# Limite d'emprunts par utilisateur (ligne ~295)
if cota > 2:  # Modifier pour changer la limite (actuellement 3)
```

### Base de données

Pour changer le nom de la base de données, modifier dans `GUI_Biblio.py` :
```python
livres = Book_Manager("test02.db")  # Modifier le nom ici
```

---

## 🐛 limitations

### Limitations actuelles

- Pas d'authentification (toute personne peut accéder à tout)
- Pas de sauvegarde/restauration de base de données
- Pas d'export de rapports (PDF, Excel)
- Pas de notifications par email

---

## 🗺️ Roadmap

### Version 1.0 (En cours)
- [x] CRUD Livres, Auteurs, Utilisateurs
- [x] Gestion basique des emprunts
- [ ] Validation des retours
- [ ] Formulaire création d'emprunt
- [ ] Historique des emprunts

### Version 2.0 (Planifiée)
- [ ] Authentification admin/lecteur
- [ ] Interface lecteur (consultation catalogue, réservations)
- [ ] Système de requêtes/réservations
- [ ] Prolongation d'emprunts
- [ ] Blocage utilisateurs retardataires

### Version 3.0 (Future)
- [ ] Statistiques avancées et rapports
- [ ] Export PDF des emprunts
- [ ] Notifications email automatiques
- [ ] API REST pour intégration externe
- [ ] Application mobile (Flutter/React Native)

---

## 👨‍💻 Auteur

**Loïc Tegofack**

- GitHub: [@Loic-Tegofack](https://github.com/Loic-Tegofack)
- Projet: [biblio-app](https://github.com/Loic-Tegofack/biblio-app)

---

## 📝 Objectifs pédagogiques

Ce projet a été développé dans un cadre d'apprentissage pour :

- ✅ Maîtriser l'architecture MVC en Python
- ✅ Apprendre la gestion de bases de données SQLite
- ✅ Créer des interfaces graphiques modernes avec CustomTkinter
- ✅ Implémenter la validation et la gestion d'erreurs
- ✅ Pratiquer Git et GitHub
- ✅ Développer une application complète de A à Z

---

## 🤝 Contributions

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -m 'Ajout fonctionnalité X'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

---

## 📄 Licence

Ce projet est développé à des fins pédagogiques et d'apprentissage.

---

## 📸 Captures d'écran


---

**⭐ Si ce projet vous a aidé, n'oubliez pas de lui donner une étoile sur GitHub !**
