# 📚 Biblio App - Système de Gestion de Bibliothèque

Application desktop de gestion de bibliothèque développée en Python avec interface graphique Tkinter.

## 🎯 Fonctionnalités

### ✅ Implémentées
- **CRUD Livres complet** : Ajout, modification, suppression et affichage
- **Gestion intelligente des auteurs** : Création automatique si l'auteur n'existe pas
- **Menu contextuel intuitif** : Clic droit sur un livre pour actions rapides
- **Validation robuste** : Vérification des données avec gestion d'erreurs
- **Architecture MVC** : Séparation claire Modèle/Vue/Contrôleur

### 🚧 En développement
- [ ] Système de gestion des emprunts
- [ ] Gestion des utilisateurs/membres
- [ ] Dashboard avec statistiques
- [ ] Recherche et filtrage avancés
- [ ] Interface moderne avec CustomTkinter

## 🛠️ Stack Technique

- **Langage** : Python 3.x
- **Interface graphique** : Tkinter
- **Base de données** : SQLite3
- **Architecture** : MVC (Model-View-Controller)

## 📦 Structure du Projet
```
biblio-app/
├── GUI_Biblio.py           # Interface graphique (Vue)
├── controleurBiblio.py     # Logique métier (Contrôleur)
├── script_sql_biblio.py    # Requêtes SQL (Modèle)
├── Biblio_model.py         # Gestion base de données
└── README.md
```

## 🚀 Installation et Lancement

### Prérequis
- Python 3.7 ou supérieur
- Tkinter (inclus avec Python sur Windows/Mac)

### Étapes
```bash
# 1. Cloner le repository
git clone https://github.com/Loic-Tegofack/biblio-app.git

# 2. Se déplacer dans le dossier
cd biblio-app

# 3. Lancer l'application
python GUI_Biblio.py
```

## 📸 Aperçu

### Interface principale
- Treeview avec liste des livres
- Menu contextuel (clic droit) pour actions rapides
- Formulaires de saisie avec validation

### Fonctionnalités clés
- **Ajout de livre** : Formulaire intelligent avec création automatique d'auteur
- **Modification** : Double-clic ou menu contextuel → édition en mode modal
- **Suppression** : Confirmation avec affichage des détails du livre

## 🎓 Objectifs Pédagogiques

Ce projet a été développé pour :
- ✅ Maîtriser la programmation orientée objet en Python
- ✅ Comprendre et implémenter l'architecture MVC
- ✅ Gérer une base de données relationnelle (SQLite)
- ✅ Créer une interface graphique complète avec Tkinter
- ✅ Appliquer les bonnes pratiques (validation, gestion d'erreurs, séparation des responsabilités)

## 🔧 Améliorations Futures

- [ ] Ajout d'une couverture de livre (images)
- [ ] Export des données (CSV, PDF)
- [ ] Historique des emprunts
- [ ] Système de réservations
- [ ] Multi-utilisateurs avec authentification
- [ ] Interface moderne (migration vers CustomTkinter)

## 📝 Licence

Projet personnel développé à des fins éducatives.

## 👤 Auteur

**Loïc Tegofack**  
[GitHub](https://github.com/Loic-Tegofack) | 

---

*Projet en cours de développement - Dernière mise à jour : Février 2025*