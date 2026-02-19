import sqlite3

class Database:
    
    def __init__(self,name_bd='biblio.db'):
        self.name_bd=name_bd
        self.create_table()

    def open_connexion(self):
        con=sqlite3.connect(self.name_bd)
        curseur=con.cursor()
        return con,curseur
    def close_connexion(self,con):
         con.close()
    
    def create_table(self):
        con,curseur = self.open_connexion()
        try:
            con.execute("PRAGMA foreign_keys = ON")  #active les cles etrangere dans la bd car desactiver par defaut
                 #creation de la table auteur
            curseur.execute(
                """ CREATE TABLE IF NOT EXISTS Auteur(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nom TEXT NOT NULL COLLATE NOCASE,
                            date_naissance INTEGER ,
                            nationalite TEXT NOT NULL COLLATE NOCASE)
                """
            )
                 #creation de la table Livres

            curseur.execute(
                """ CREATE TABLE IF NOT EXISTS Livre(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            auteur_id INTEGER,
                            titre TEXT NOT NULL COLLATE NOCASE,
                            date INTEGER,     
                            genre TEXT COLLATE NOCASE,
                            etat TEXT NOT NULL COLLATE NOCASE,
                            nbre_exemplaire INTEGER NOT NULL,
                            FOREIGN KEY(auteur_id) REFERENCES Auteur(id))
                """
             )
                #creation de la table Utilisateur
            curseur.execute(
                    """ CREATE TABLE IF NOT EXISTS Utilisateur(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nom TEXT NOT NULL COLLATE NOCASE,
                                prenom TEXT NOT NULL COLLATE NOCASE,
                                adresse TEXT COLLATE NOCASE,
                                status TEXT,
                                mdp TEXT NOT NULL UNIQUE)
                    """
                )
                #creation de la table des emprunts
            curseur.execute(
                    """ CREATE TABLE IF NOT EXISTS Emprunt(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                livre_id INTEGER,
                                utilisateur_id INTEGER,
                                date_emprunt TEXT NOT NULL,
                                date_retour TEXT NOT NULL,
                                status TEXT,
                                FOREIGN KEY(livre_id) REFERENCES Livre(id),
                                FOREIGN KEY(utilisateur_id) REFERENCES Utilisateur(id)
                                )
                    """
                )
        finally:
            self.close_connexion(con)
            
                
    







