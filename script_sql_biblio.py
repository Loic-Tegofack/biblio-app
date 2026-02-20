
from Biblio_model import Database

#Fonctions de Gestion De la table Auteur
class Auteur:
    def __init__(self,bd):
        self.bd=Database(bd)
        #Recherche  identifiant d'un auteur 
    def search_auteur(self,nom):
        con,curseur = self.bd.open_connexion()
        try:
            with con:
                curseur.execute(
                            """
                            SELECT id FROM Auteur WHERE nom=? 
                            """,(nom,)
                        )
                id_a=curseur.fetchone()
        finally:
               self.bd.close_connexion(con)
        return id_a[0] if id_a else None
        
        #Ajout d'un auteur
    def new_author(self,nom_auteur,date_auteur,pays_auteur):
        con,curseur= self.bd.open_connexion()
        try:
           with con:
                curseur.execute(
                    """
                    INSERT INTO Auteur(nom,date_naissance ,nationalite ) VALUES(?,?,?)
                    """,(nom_auteur,date_auteur,pays_auteur)
                )
                id_e=curseur.lastrowid
        finally:
           self.bd.close_connexion(con)
        return id_e
       
        #Affiche les infos d'un auteur selectionne
    def author(self,id_auteur):
        con,curseur=self.bd.open_connexion()
        result=None
        try:
            with con:
                curseur.execute(
                    """
                     SELECT nom, date_naissance, nationalite  FROM Auteur WHERE id=?
                    """,(id_auteur,)
                )
                result=curseur.fetchone()
        finally:
            self.bd.close_connexion(con)
        return result
    
    def display_author(self):
        con,curseur=self.bd.open_connexion()
        result=None
        try:
            with con:
                curseur.execute(
                    """
                     SELECT id,nom, date_naissance, nationalite  FROM Auteur 
                    """
                )
                result=curseur.fetchall()
        finally:
            self.bd.close_connexion(con)
        return result

    
    def delete_author(self,id):
        con,curseur=self.bd.open_connexion()
        try:
            with con:
                curseur.execute(
                    """
                     DELETE FROM Auteur WHERE id=?
                    """,(id,)
                )
        finally:
            self.bd.close_connexion(con)
        return True
    def a_au_moins_un_livre(self,id):
        con,curseur=self.bd.open_connexion()
        nbre=None
        try:
            with con:
                curseur.execute(
                    """
                     SELECT COUNT(Livre.id) FROM Livre INNER JOIN Auteur ON Livre.auteur_id=Auteur.id WHERE Auteur.id=?
                    """,(id,)
                )
                nbre=curseur.fetchone()
        finally:
            self.bd.close_connexion(con)
        return nbre[0] if nbre else None



  
#Fonctions de Gestions de la table Livre

class Livre:
    def __init__(self,bd):
        self.bd=Database(bd)
       #Ajout d'un Livre
    def add_book(self,titre_livre,id_auteur,etat,date,genre,exemplaire):
         con,curseur= self.bd.open_connexion()
         try:
            with con:
                curseur.execute(
                    """
                     INSERT INTO Livre(auteur_id,titre,date,genre,etat,nbre_exemplaire ) VALUES(?,?,?,?,?,?)
                    """,(id_auteur,titre_livre,date,genre,etat,exemplaire)
                    )       
         finally:
            self.bd.close_connexion(con)
     
        #Recherche d'un Livre(son ID)
    def get_id_book(self,titre):
        con,curseur=self.bd.open_connexion()
        try:
            with con:
                curseur.execute(
                    """
                    SELECT id FROM Livre WHERE titre=? 
                    """,(titre,)
                )
                id_livre=curseur.fetchone()
        finally:
                self.bd.close_connexion(con)
        return id_livre[0] if id_livre else None

       #Suppression d'un Livre 
    def delete_book(self,idf):
        con,curseur=self.bd.open_connexion()
        try:
            with con:
                curseur.execute(
                    """
                    DELETE FROM Livre  WHERE id=?
                    """,(idf,)
                )
        finally:
             self.bd.close_connexion(con)

       #Modification d'un Livre
    def update_book(self,boo_id,book_modification): 
        champs=[]
        valeurs=[]
        for champ,valeur in book_modification.items(): 
            champs.append(f"{champ}=?")
            valeurs.append(valeur)

        valeurs.append(boo_id)
        sql= f" UPDATE Livre SET {','.join(champs)} WHERE id=?"


        con,curseur=self.bd.open_connexion()
        try:
            with con:
                curseur.execute(sql,valeurs)
        finally:
            self.bd.close_connexion(con)
    
        #renvoie la liste complete de toute les livres stocker en BD et leurs informations
    def display_book(self):  
        con,curseur=self.bd.open_connexion()
        try:
            with con:
                curseur.execute(
                    """
                    SELECT Livre.id,Auteur.nom,titre,date,genre,etat,nbre_exemplaire FROM Livre INNER JOIN Auteur ON Auteur.id=auteur_id
                    """
                )
                livre = curseur.fetchall()
        finally:
            self.bd.close_connexion(con)
        return livre
          #verifier si un livre existe et renvoir true si oui et false sinon
    def book_exist_or_not(self,idr):   
        con,curseur=self.bd.open_connexion()
        resultat=None
        try:
            with con:
                curseur.execute(
                    """
                    SELECT 1 FROM Livre WHERE id=?
                    """,(idr,)
                )
                resultat = curseur.fetchone()
        finally:
            self.bd.close_connexion(con)
        return resultat is not None 
    
            #renvoir les informations sur un livre specifique(son ID)
    def search_book(self,id_book):
        con,curseur=self.bd.open_connexion()
        trouver=None
        try:
            with con:
                curseur.execute(
                    """
                    SELECT Auteur.nom,titre,date,genre,etat, nbre_exemplaire FROM Livre INNER JOIN Auteur ON Auteur.id=auteur_id WHERE Livre.id=?
                    """,(id_book,)
                )
                trouver = curseur.fetchone()
        finally:
           self.bd.close_connexion(con)
        return trouver

            #Gestion de l'emprunt d'un livre
"""def borrow_book():
    con,curseur=open_connexion()
    curseur.execute(
        
    )
    trouver = curseur.fetchone()
    close_connexion(con)"""""

#Fonctions de Gestions des utilisateur
  
class Utilisateurs:
    def __init__(self,bd):
        self.bd=Database(bd)
              #ajout d'un utilisateur
    def create_user(self,nom,prenom,adresse,status,mdp):
        con,curseur=self.bd.open_connexion()
        try:
            with con:
                curseur.execute(
                    """
                    INSERT INTO Utilisateur (nom,prenom,adresse,status,mdp) VALUES (?,?,?,?,?)
                    """,(nom,prenom,adresse,status,mdp)
                )
        finally:
            self.bd.close_connexion(con)
    
              #Display User
    def display_user(self):
        con,curseur=self.bd.open_connexion()
        result=None
        try:
            with con:
                curseur.execute(
                    """
                    SELECT * FROM Utilisateur 
                    """
                )
                result=curseur.fetchall()
            
        finally:
            self.bd.close_connexion(con)
        return result
    
              #Chercher un utilisateur
    def user_search(self,id_user):
        con,curseur=self.bd.open_connexion()
        try:
            with con:
                curseur.execute(
                    """
                    SELECT * FROM Utilisateur WHERE id=? 
                    """,(id_user,)
                )
                result=curseur.fetchone()
        finally:
           self.bd.close_connexion(con)
        return result if result else None
    
              #recupere l'ID de utilisateur
    def user_id(self,nom,prenom):
      con,curseur=self.bd.open_connexion()
      try:
            with con:
                curseur.execute(
                    """
                    SELECT id FROM Utilisateur WHERE nom=? AND prenom=?
                    """,(nom,prenom)
                )
                id_user=curseur.fetchone()
      finally:
          self.bd.close_connexion(con)
      return id_user[0] if id_user else None
   
              #supprimer un utilisateur
    def delete_user(self,id_delete):
        con,curseur=self.bd.open_connexion()
        try:
            with con:
                curseur.execute(
                    """
                    DELETE FROM Utilisateur WHERE id =? 
                    """,(id_delete,)
                )
        finally:
            self.bd.close_connexion(con)
        

    
