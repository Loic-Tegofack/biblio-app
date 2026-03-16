"""
populate_biblio.py
==================
Script de peuplement de la base de données pour tester la partie utilisateur.

COMMENT L'UTILISER :
--------------------
1. Place ce fichier dans le même dossier que tes autres fichiers Python
2. Lance-le UNE seule fois :  python populate_biblio.py
3. Lance ensuite ton application normalement : python GUI_Biblio.py

COMPTES CRÉÉS :
---------------
  ADMIN
  ├─ Nom     : Admin
  ├─ Prénom  : Super
  └─ Mdp     : admin123

  UTILISATEURS
  ├─ Martin   / Alice    — mdp : alice123   (aucun emprunt)
  ├─ Dupont   / Thomas   — mdp : thomas123  (1 emprunt en cours, dans les délais)
  ├─ Bernard  / Sophie   — mdp : sophie123  (2 emprunts en cours, dont 1 EN RETARD)
  └─ Leblanc  / Marc     — mdp : marc123    (quota max atteint : 3 emprunts actifs)

CE QUE TU PEUX TESTER :
------------------------
  - Connexion admin / utilisateur
  - Vue catalogue livres (côté user)
  - Emprunt normal (avec Alice)
  - Emprunt bloqué par retard (avec Sophie)
  - Emprunt bloqué par quota (avec Marc)
  - Retour d'un livre (avec Thomas)
  - Historique d'emprunts
  - Gestion des utilisateurs (côté admin)
"""

import sqlite3
import hashlib
from datetime import date, timedelta

# ─── CONFIGURATION ────────────────────────────────────────────────────────────
NOM_BD = "test01.db"  # Doit correspondre au nom utilisé dans GUI_Biblio.py

# ─── UTILITAIRES ──────────────────────────────────────────────────────────────

def hacher(mdp: str) -> str:
    """Hache un mot de passe en SHA-256, comme le fait controleurBiblio.py."""
    return hashlib.sha256(mdp.encode()).hexdigest()

def creer_connexion():
    con = sqlite3.connect(NOM_BD)
    con.execute("PRAGMA foreign_keys = ON")
    return con

# ─── DONNÉES ──────────────────────────────────────────────────────────────────

AUTEURS = [
    # (nom, prenom, date_naissance, nationalite)
    ("Hugo",       "Victor",    1802, "Française"),
    ("Camus",      "Albert",    1913, "Française"),
    ("Orwell",     "George",    1903, "Britannique"),
    ("Rowling",    "J.K.",      1965, "Britannique"),
    ("Dostoïevski","Fiodor",    1821, "Russe"),
    ("Zola",       "Émile",     1840, "Française"),
    ("Saint-Exupéry", "Antoine", 1900, "Française"),
]

LIVRES = [
    # (titre, auteur_idx, date, genre, etat, nbre_exemplaire)
    # auteur_idx correspond à la position dans AUTEURS (commence à 0)
    ("Les Misérables",          0, 1862, "Roman",     "Disponible", 3),
    ("Notre-Dame de Paris",     0, 1831, "Roman",     "Disponible", 2),
    ("L'Étranger",              1, 1942, "Roman",     "Disponible", 4),
    ("La Peste",                1, 1947, "Roman",     "Disponible", 2),
    ("1984",                    2, 1949, "Dystopie",  "Disponible", 3),
    ("La Ferme des animaux",    2, 1945, "Dystopie",  "Disponible", 2),
    ("Harry Potter T1",         3, 1997, "Fantastique","Disponible", 5),
    ("Harry Potter T2",         3, 1998, "Fantastique","Disponible", 3),
    ("Crime et Châtiment",      4, 1866, "Roman",     "Disponible", 2),
    ("Germinal",                5, 1885, "Roman",     "Disponible", 2),
    ("Le Petit Prince",         6, 1943, "Conte",     "Disponible", 6),
    ("Vol de Nuit",             6, 1931, "Roman",     "Disponible", 1),
]

UTILISATEURS = [
    # (nom, prenom, adresse, mdp_clair, status)
    ("Admin",   "Super",  "1 rue de l'admin",       "admin123",  "admin"),
    ("Martin",  "Alice",  "12 rue des Lilas",        "alice123",  "user"),
    ("Dupont",  "Thomas", "5 avenue Victor Hugo",    "thomas123", "user"),
    ("Bernard", "Sophie", "8 boulevard Saint-Michel","sophie123", "user"),
    ("Leblanc", "Marc",   "3 impasse des Roses",     "marc123",   "user"),
]

# ─── CRÉATION DES TABLES ──────────────────────────────────────────────────────

def creer_tables(con):
    con.executescript("""
        CREATE TABLE IF NOT EXISTS Auteur(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL COLLATE NOCASE,
            prenom TEXT COLLATE NOCASE,
            date_naissance INTEGER,
            nationalite TEXT COLLATE NOCASE
        );

        CREATE TABLE IF NOT EXISTS Livre(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            auteur_id INTEGER,
            titre TEXT NOT NULL COLLATE NOCASE,
            date INTEGER,
            genre TEXT COLLATE NOCASE,
            etat TEXT NOT NULL COLLATE NOCASE,
            nbre_exemplaire INTEGER NOT NULL,
            FOREIGN KEY(auteur_id) REFERENCES Auteur(id)
        );

        CREATE TABLE IF NOT EXISTS Utilisateur(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL COLLATE NOCASE,
            prenom TEXT NOT NULL COLLATE NOCASE,
            adresse TEXT COLLATE NOCASE,
            mdp TEXT NOT NULL UNIQUE,
            status TEXT
        );

        CREATE TABLE IF NOT EXISTS Emprunt(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livre_id INTEGER,
            utilisateur_id INTEGER,
            date_emprunt TEXT NOT NULL,
            date_retour_effective TEXT,
            date_retour_prevue TEXT,
            FOREIGN KEY(livre_id) REFERENCES Livre(id) ON DELETE RESTRICT,
            FOREIGN KEY(utilisateur_id) REFERENCES Utilisateur(id) ON DELETE RESTRICT
        );
    """)
    con.commit()
    print("  Tables vérifiées / créées.")

# ─── INSERTION ────────────────────────────────────────────────────────────────

def inserer_auteurs(con) -> list:
    """Insère les auteurs et retourne leurs IDs dans l'ordre d'insertion."""
    ids = []
    curseur = con.cursor()
    for nom, prenom, naissance, pays in AUTEURS:
        curseur.execute(
            "INSERT OR IGNORE INTO Auteur(nom,prenom,date_naissance,nationalite) VALUES(?,?,?,?)",
            (nom, prenom, naissance, pays)
        )
        # Récupère l'id qu'il vient d'être inséré OU qui existait déjà
        curseur.execute("SELECT id FROM Auteur WHERE nom=? AND prenom=?", (nom, prenom))
        ids.append(curseur.fetchone()[0])
    con.commit()
    print(f"  {len(ids)} auteurs insérés.")
    return ids

def inserer_livres(con, ids_auteurs: list) -> list:
    """Insère les livres et retourne leurs IDs."""
    ids = []
    curseur = con.cursor()
    for titre, auteur_idx, annee, genre, etat, exemplaires in LIVRES:
        auteur_id = ids_auteurs[auteur_idx]
        curseur.execute(
            """INSERT OR IGNORE INTO Livre(auteur_id,titre,date,genre,etat,nbre_exemplaire)
               VALUES(?,?,?,?,?,?)""",
            (auteur_id, titre, annee, genre, etat, exemplaires)
        )
        curseur.execute("SELECT id FROM Livre WHERE titre=?", (titre,))
        ids.append(curseur.fetchone()[0])
    con.commit()
    print(f"  {len(ids)} livres insérés.")
    return ids

def inserer_utilisateurs(con) -> list:
    """Insère les utilisateurs avec mots de passe hachés et retourne leurs IDs."""
    ids = []
    curseur = con.cursor()
    for nom, prenom, adresse, mdp_clair, status in UTILISATEURS:
        mdp_hache = hacher(mdp_clair)
        curseur.execute(
            """INSERT OR IGNORE INTO Utilisateur(nom,prenom,adresse,mdp,status)
               VALUES(?,?,?,?,?)""",
            (nom, prenom, adresse, mdp_hache, status)
        )
        curseur.execute("SELECT id FROM Utilisateur WHERE nom=? AND prenom=?", (nom, prenom))
        ids.append(curseur.fetchone()[0])
    con.commit()
    print(f"  {len(ids)} utilisateurs insérés.")
    return ids

def inserer_emprunts(con, ids_livres: list, ids_users: list):
    """
    Crée des emprunts scénarisés pour tester les règles métier.

    ids_users[0] = Admin/Super     → pas d'emprunt
    ids_users[1] = Martin/Alice    → pas d'emprunt (peut emprunter librement)
    ids_users[2] = Dupont/Thomas   → 1 emprunt en cours, dans les délais
    ids_users[3] = Bernard/Sophie  → 2 emprunts dont 1 EN RETARD
    ids_users[4] = Leblanc/Marc    → 3 emprunts actifs (quota max atteint)
    """
    curseur = con.cursor()
    aujourd_hui = date.today()

    emprunts = [
        # ── Thomas : 1 emprunt normal en cours ──────────────────────────────
        # livre: L'Étranger (ids_livres[2]), emprunté il y a 5 jours
        {
            "livre_id":      ids_livres[2],
            "user_id":       ids_users[2],
            "date_emprunt":  str(aujourd_hui - timedelta(days=5)),
            "date_prevue":   str(aujourd_hui + timedelta(days=9)),  # dans 9 jours
            "date_effective": None,
        },

        # ── Sophie : emprunt 1 — dans les délais ────────────────────────────
        {
            "livre_id":      ids_livres[4],   # 1984
            "user_id":       ids_users[3],
            "date_emprunt":  str(aujourd_hui - timedelta(days=3)),
            "date_prevue":   str(aujourd_hui + timedelta(days=11)),
            "date_effective": None,
        },
        # ── Sophie : emprunt 2 — EN RETARD (prévu il y a 5 jours) ───────────
        {
            "livre_id":      ids_livres[6],   # Harry Potter T1
            "user_id":       ids_users[3],
            "date_emprunt":  str(aujourd_hui - timedelta(days=21)),
            "date_prevue":   str(aujourd_hui - timedelta(days=7)),  # dépassé !
            "date_effective": None,
        },

        # ── Marc : 3 emprunts actifs = quota max ────────────────────────────
        {
            "livre_id":      ids_livres[0],   # Les Misérables
            "user_id":       ids_users[4],
            "date_emprunt":  str(aujourd_hui - timedelta(days=10)),
            "date_prevue":   str(aujourd_hui + timedelta(days=4)),
            "date_effective": None,
        },
        {
            "livre_id":      ids_livres[8],   # Crime et Châtiment
            "user_id":       ids_users[4],
            "date_emprunt":  str(aujourd_hui - timedelta(days=7)),
            "date_prevue":   str(aujourd_hui + timedelta(days=7)),
            "date_effective": None,
        },
        {
            "livre_id":      ids_livres[10],  # Le Petit Prince
            "user_id":       ids_users[4],
            "date_emprunt":  str(aujourd_hui - timedelta(days=2)),
            "date_prevue":   str(aujourd_hui + timedelta(days=12)),
            "date_effective": None,
        },

        # ── Historique : un emprunt déjà rendu (pour tester l'historique) ───
        {
            "livre_id":      ids_livres[11],  # Vol de Nuit
            "user_id":       ids_users[1],    # Alice
            "date_emprunt":  str(aujourd_hui - timedelta(days=30)),
            "date_prevue":   str(aujourd_hui - timedelta(days=16)),
            "date_effective": str(aujourd_hui - timedelta(days=18)),  # rendu à temps
        },
    ]

    for e in emprunts:
        curseur.execute(
            """INSERT OR IGNORE INTO Emprunt
               (livre_id, utilisateur_id, date_emprunt, date_retour_effective, date_retour_prevue)
               VALUES (?,?,?,?,?)""",
            (e["livre_id"], e["user_id"], e["date_emprunt"],
             e["date_effective"], e["date_prevue"])
        )
        # Met à jour le stock si l'emprunt est actif
        if e["date_effective"] is None:
            curseur.execute(
                "UPDATE Livre SET nbre_exemplaire = nbre_exemplaire - 1 WHERE id = ? AND nbre_exemplaire > 0",
                (e["livre_id"],)
            )

    con.commit()
    print(f"  {len(emprunts)} emprunts insérés.")

# ─── RÉSUMÉ ───────────────────────────────────────────────────────────────────

def afficher_resume(con):
    curseur = con.cursor()
    print("\n" + "═" * 55)
    print("  RÉSUMÉ DE LA BASE DE DONNÉES")
    print("═" * 55)

    curseur.execute("SELECT COUNT(*) FROM Auteur")
    print(f"  Auteurs       : {curseur.fetchone()[0]}")

    curseur.execute("SELECT COUNT(*) FROM Livre")
    print(f"  Livres        : {curseur.fetchone()[0]}")

    curseur.execute("SELECT COUNT(*) FROM Utilisateur")
    print(f"  Utilisateurs  : {curseur.fetchone()[0]}")

    curseur.execute("SELECT COUNT(*) FROM Emprunt WHERE date_retour_effective IS NULL")
    print(f"  Emprunts actifs : {curseur.fetchone()[0]}")

    curseur.execute(
        "SELECT COUNT(*) FROM Emprunt WHERE date_retour_effective IS NULL AND date_retour_prevue < date('now')"
    )
    print(f"  Emprunts en retard : {curseur.fetchone()[0]}")

    print("\n  COMPTES DE CONNEXION :")
    print("  ┌─────────────────────────────────────────────┐")
    for nom, prenom, _, mdp_clair, status in UTILISATEURS:
        role = "👑 admin" if status == "admin" else "👤 user "
        print(f"  │  {role}  {nom:<10} {prenom:<10}  mdp: {mdp_clair:<12} │")
    print("  └─────────────────────────────────────────────┘")

    print("\n  SCÉNARIOS DE TEST :")
    print("  • Alice   → peut emprunter normalement")
    print("  • Thomas  → 1 emprunt en cours (peut encore emprunter)")
    print("  • Sophie  → 1 emprunt EN RETARD → emprunt bloqué")
    print("  • Marc    → quota de 3 atteint → emprunt bloqué")
    print("═" * 55 + "\n")

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print(f"\nPopulation de la base : {NOM_BD}")
    print("─" * 40)

    con = creer_connexion()
    try:
        creer_tables(con)
        ids_auteurs    = inserer_auteurs(con)
        ids_livres     = inserer_livres(con, ids_auteurs)
        ids_utilisateurs = inserer_utilisateurs(con)
        inserer_emprunts(con, ids_livres, ids_utilisateurs)
        afficher_resume(con)
    except Exception as e:
        print(f"\n  ERREUR : {e}")
        con.rollback()
    finally:
        con.close()

if __name__ == "__main__":
    main()