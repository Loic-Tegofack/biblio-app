
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
                    SELECT Auteur.nom,titre,date,genre,etat, nbre_exemplaire 
                    FROM Livre INNER JOIN Auteur ON Auteur.id=auteur_id WHERE Livre.id=?
                    """,(id_book,)
                )
                trouver = curseur.fetchone()
        finally:
           self.bd.close_connexion(con)
        return trouver

#Fonctions de Gestions des utilisateur
  
class Utilisateurs:
    def __init__(self,bd):
        self.bd=Database(bd)
              #ajout d'un utilisateur
    def create_user(self,nom,prenom,adresse,mdp):
        con,curseur=self.bd.open_connexion()
        try:
            with con:
                curseur.execute(
                    """
                    INSERT INTO Utilisateur (nom,prenom,adresse,mdp) VALUES (?,?,?,?)
                    """,(nom,prenom,adresse,mdp)
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

class EMPRUNT:
    def __init__(self,bd):
        self.bd=Database(bd)
    
    def afficher_emprunts(self):
        con,curseur=self.bd.open_connexion()
        result=0
        try:
            with con:
                curseur.execute(
                    """
                    SELECT Utilisateur.nom,Livre.titre,Emprunt.date_emprunt, Emprunt.date_retour_effective,Emprunt.date_retour_prevue 
                    FROM Emprunt INNER JOIN Utilisateur ON Utilisateur.id=Emprunt.utilisateur_id
                    INNER JOIN Livre ON Livre.id = Emprunt.livre_id WHERE Emprunt.date_retour_effective IS NULL
            
                    """
                )
                result=curseur.fetchall()
        finally:
            self.bd.close_connexion(con)
        return result

    def nbre_livre_emprunter_Par_un_utilisateur(self,id):
        con,curseur=self.bd.open_connexion()
        result=[]
        try:
            with con:
                curseur.execute(
                    """
                     SELECT COUNT(E.livre_id) FROM Emprunt as E
                     WHERE E.utilisateur_id = ? AND E.date_retour_effective IS NULL
            
                    """,(id,)
                )
                result=curseur.fetchone()
        finally:
            self.bd.close_connexion(con)
        return result[0] if result else 0
        
    def historique_emprunts_utilisateur(self,id):
        con,curseur=self.bd.open_connexion()
        result=[]
        try:
            with con:
                curseur.execute(
                    """
                     SELECT E.livre_id,L.titre FROM Emprunt as E
                     INNER JOIN Livre as L ON L.id=E.livre_id
                     WHERE E.utilisateur_id = ?
            
                    """,(id,)
                )
                result=curseur.fetchall()
        finally:
            self.bd.close_connexion(con)
        return result
    
        
    def emprunts_encours(self,id):
        con,curseur=self.bd.open_connexion()
        result=[]
        try:
            with con:
                curseur.execute(
                    """
                     SELECT E.livre_id,L.titre FROM Emprunt as E
                     INNER JOIN Livre as L ON L.id=E.livre_id
                     WHERE E.utilisateur_id = ? AND  E.date_retour_effective IS NULL
            
                    """,(id,)
                )
                result=curseur.fetchall()
        finally:
            self.bd.close_connexion(con)
        return result
    
    def ajouter_emprunt(self,id_user,id_book,current_date,borrow_return):
        con,curseur=self.bd.open_connexion()
        result=0
        try:
            with con:
                curseur.execute(
                    """
                     INSERT INTO Emprunt (livre_id,utilisateur_id, date_emprunt,date_retour_effective,date_retour_prevue)
                     VALUES (?,?,?,?,?)
            
                    """,(id_book,id_user,current_date,None,borrow_return)
                )
#mise a jour de la table Livre si le livre est emprunte
                curseur.execute(
                    """
                     UPDATE Livre SET nbre_exemplaire  = nbre_exemplaire - 1 WHERE Livre.id = ? AND nbre_exemplaire > 0
                    """,(id_book,)
                )
                result=curseur.rowcount
                
        finally:
            self.bd.close_connexion(con)
        return result #si result=0 emprunt echoue | si result = 1 emprunt reussie
    
    def livre_deja_emprunter(self,id_book,id_user):#cette fonction permet d'empecher un utilisateur d'emprunter un meme exempalire d'un livre 02 fois de suite
        con,curseur=self.bd.open_connexion()
        result=None
        try:
            with con:
                curseur.execute(
                    """
                     SELECT 1 FROM Emprunt
                     WHERE Emprunt.livre_id=? AND utilisateur_id = ? AND Emprunt.date_retour_effective IS  NULL LIMIT 1 
            
                    """,(id_book,id_user)
                )
                result=curseur.fetchone() # SI la fonction retourne 1 alors ce livre ne peut-etre emprunter car deja emprunter
                
        finally:
            self.bd.close_connexion(con)
        return result[0] if result else 0
    
    def valider_retour(self,id_book,id_user):
        con,curseur=self.bd.open_connexion()
        try:
            with con:
#On calcul le retard a la remise du livre, si retard > 0 , alors livre remis en retard sinon remis en avance
                curseur.execute(
                    """
                    SELECT JULIANDAY ('now') - JULIANDAY( date_retour_prevue )
                    FROM Emprunt WHERE date_retour_effective IS NULL AND livre_id = ?  AND utilisateur_id = ?
                    """,(id_book,id_user)
                )
                result=curseur.fetchone()

                retard = result[0] if result else None
#on met a jour la table d'emprunt apres un retour valider, si la requete est execute alors nbre_modif renvoie le nombre de ligne modifier
#sinon il renvoi 0 et alors on conclu que ce livre n'a pas ete emprunter
                curseur.execute(
                    """
                       UPDATE Emprunt SET date_retour_effective = date('now')
                       WHERE livre_id = ? AND utilisateur_id = ?  AND date_retour_effective IS NULL
                    """,(id_book,id_user)
                )
                nbre_modif=curseur.rowcount

                if nbre_modif > 0:
                
                    curseur.execute(
                        """
                        UPDATE Livre SET   nbre_exemplaire =   nbre_exemplaire + 1 WHERE Livre.id = ?
                        """ ,(id_book,)
                    )
                
        finally:
            self.bd.close_connexion(con)
        return (nbre_modif,retard)
    
    def a_des_retard(self,id_user):
        con,curseur=self.bd.open_connexion()
        result=None
        try:
            with con:
                    curseur.execute(
                        """
                        SELECT COUNT(*) FROM Emprunt 
                        WHERE utilisateur_id = ? 
                        AND date_retour_effective IS NULL 
                        AND date_retour_prevue < date('now')
                        """,(id_user,)
                    )
                    result=curseur.fetchone() # SI la fonction retourne 1 alors ce livre ne peut-etre emprunter car deja emprunter
                
        finally:
            self.bd.close_connexion(con)
        return result[0] if result else 0

    


        
    
