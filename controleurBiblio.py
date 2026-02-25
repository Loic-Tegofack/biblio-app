from script_sql_biblio import Auteur,Livre,Utilisateurs,EMPRUNT
from datetime import date,timedelta
import hashlib
#Fonctions de Gestion Des auteurs

class Author_Manager: #Il faudrai une fonction de modification au cas ou les donnees aurait ete mal saisi
    def __init__(self,bd):
        self.bd=bd
        self.auteur=Auteur(self.bd)
        
   #Ici on verifie si l'auteur existe deja sinon on le creer et on renvoie ses informations
    def get_or_create_auteur(self,nom,naissance,pays): 
        nd=None 
        if not nom or not nom.strip():   
            raise ValueError("La saisi du nom est Obligatoire !")
        if naissance:
              try:
                nd=int(naissance)
                if nd<0:
                    raise ValueError("Entrer une valeur correct !")
              except ValueError:
                raise ValueError("la date de naissance doit etre un nombre")
        id_auteur = self.auteur.search_auteur(nom)
        if id_auteur is None:
          return self.auteur.new_author(nom,nd,pays)
        else:
            return self.auteur.author(id_auteur)
    
    def retourne_id_auteur(self,nom):
        if not nom  or not nom.strip():
            raise ValueError("Veuillez renseigner le nom de l'auteur")
        author=self.auteur.search_auteur(nom)
        if author is None:
            return None
        return author
    
    def rechercher_auteur(self,nom):
        if not nom  or not nom.strip():
            raise ValueError("Veuillez renseigner le nom de l'auteur")
        id=self.auteur.search_auteur(nom)
        if id is None:
            return None
        infos=self.auteur.author(id)
        return infos if infos else None

    def supprimer_auteur(self,nom):
        if not nom or not nom.strip():
            raise ValueError("Veuillez renseigner le nom de l'auteur")
        id_auteur=self.auteur.search_auteur(nom)
        if not id_auteur:
            raise ValueError("Auteur Inexistant !")
        nbre_livre=self.auteur.a_au_moins_un_livre(id_auteur)
        if nbre_livre:
            raise ValueError("Cet auteur ne peut etre supprimer\n car il a ecrit au moins un livre !")
        self.auteur.delete_author(id_auteur)
        return True
    
    def afficher_auteur(self):
        auteurs=self.auteur.display_author()
        return auteurs
    def recherche_auteur_par_id(self,id):
        if not id:
            return None
        infos=self.auteur.author(id)
        return infos if infos else None



#Fonctions de Gestion Des livres
   
class Book_Manager:
    def __init__(self,bd):
        self.bd=bd
        self.livre=Livre(self.bd)
        self.auteur=Author_Manager(self.bd)
     #Ajout d'un Livre
    def ajouter_livre(self,titre,auteur_name,date_auteur,country_auteur,etat,date=None,exemplaire=None,genre=None):
        val_date=None
        val_exemplaire=0
        if not all([etat,titre]):
            raise ValueError("le titre et l'etat sont obligatoires !!!") 
        if date:
                try:
                  val_date=int(date)
                  if val_date<0:
                    raise ValueError("Veuillez entrer une date positif !")
                except ValueError:
                    raise ValueError("La date doit etre un nombre!!!")
        if exemplaire:
            try:
                val_exemplaire=int(exemplaire)
                if val_exemplaire<0:
                 raise ValueError ("Le nombre d'exemplaire doit etre positif")
            except ValueError:
                    raise ValueError("Le nombre d'exemplaire doit etre un nombre!!!")
        id_book=self.livre.get_id_book(titre)
        if self.livre.book_exist_or_not(id_book):
            return self.livre.search_book(id_book)
        auteur_id=self.auteur.rechercher_auteur(auteur_name)
        if auteur_id is None:
            self.auteur.get_or_create_auteur(auteur_name,date_auteur,country_auteur)
            auteur_id=self.auteur.retourne_id_auteur(auteur_name)
        self.livre.add_book(titre,auteur_id,etat,val_date,genre,val_exemplaire)
        return True
        
    #Affichage de tous les Livre de la BD         
    def afficher_livre(self):
      return self.livre.display_book()

    #Suppression d'un Livre en particulier
    def supprimer_livre(self,nom_livre):
        if not nom_livre:
                raise ValueError("Veuillez saisir le titre du livre a supprimer")
        ids=self.livre.get_id_book(nom_livre)
        if ids is None:  # la on verifie d'abord que le livre existe avant de supprimer
            return None
        self.livre.delete_book(ids)
        return True
       
      #Modification d'un Livre
    def modifier_livre(self,id_livre,nouveau_titre=None,date=None,genre=None,etat=None,exemplaire=None):
        exemplaires=0
        modification={}
        if id_livre is None:
            raise ValueError("Action impossible car ce Livre n'es pas enregistrer")
        if nouveau_titre:
            modification["titre"]=nouveau_titre
        dates=None
        if date:
            try:
              dates=int(date)
              if dates<0:
                    raise ValueError("Veuillez entrer une date positif !")
              modification["date"]=dates    
            except ValueError:
                raise ValueError("La date doit etre un nombre!!!")
        if genre:
            modification["genre"]=genre
        if etat:
            modification["etat"]=etat
        if exemplaire is not None :
            try:
                exemplaires=int(exemplaire)
                if exemplaires<0:
                  raise ValueError( "Le nombre d'exemplaire doit etre positif")
                modification["nbre_exemplaire"]=exemplaires
            except ValueError:
                    raise ValueError("ERREUR : Le nombre d'exemplaire doit etre un nombre!!!")
        
        if not modification:
            return False
    
        self.livre.update_book(id_livre,modification)
        return True

           #Recherche d'un Livre
    def rechercher(self,nom_livre):
        if not nom_livre:
            raise ValueError("Veuillez saisir le titre du livre chercher")
        idr=self.livre.get_id_book(nom_livre)
        if idr is None:  
            return None
        resultat=self.livre.search_book(idr)
        return resultat
    def recherche_par_id(self,id_livre):
        if not id_livre:
            raise ValueError("Livres introuvable !")
        resultat=self.livre.search_book(id_livre)
        return resultat
    def book_id(self,titre):
        return self.livre.get_id_book(titre)
    
        

#Fonctions de Gestions des utilisateur

class User_Manager:
    def __init__(self,bd):
        self.bd=bd
        self.utilisateurs=Utilisateurs(self.bd)
             #supprimer un utilisateur
    def delete_utilisateur(self,nom_user,prenom_user):
        if not all((nom_user,prenom_user)):
            raise ValueError( "Le nom et le prenom sont obligatoire pour effectuer cette operation !!!")
        ID_USER=self.utilisateurs.user_id(nom_user,prenom_user) # 2. On récupère l'ID une seule fois
        if ID_USER is None:
            raise ValueError("Action Impossible, Utilisateur inexistant !! |")
        
        self.utilisateurs.delete_user(ID_USER)
        return True # On renvoie True pour confirmer que tout s'est bien passé
           
                    #Ajout d'un utilisateur
    def ajout_utilisateur(self,nom="Inconnue",prenom="Inconnue",adresse=None,mdp=None):

        mdp_hache=hashlib.sha256(mdp.encode()).hexdigest()

        if self.utilisateurs.user_id(nom,prenom) is not None:
            raise ValueError(f"{nom} {prenom} est deja enregistrer!!") 
        if not all ([nom,prenom,adresse,mdp]):
            raise ValueError("Veuillez rempli tous les champs !!!") 
        if nom.lower() == prenom.lower() :
            raise ValueError(f"Nom doit etre different du prenom") 
        if len(mdp)<6:
            raise ValueError("Mot de passe trop courte veuillez ressayer !!")   
        return self.utilisateurs.create_user(nom,prenom,adresse,mdp_hache)
        
                    #Recherche d'un UTilisateur
    def rechercher_utilisateur(self,name=None,surname=None):
        if not name or not surname:
            raise ValueError ("Le nom et le prénom sont obligatoires pour la recherche !!") 
        
        ID= self.utilisateurs.user_id(name,surname)
        if ID is None:
            return None
        return  self.utilisateurs.user_search(ID)
                    #Liste de tous les utilisateur enregistrer
    def display_utilisateur(self):
    
        return  self.utilisateurs.display_user()
    
    def retourne_id_utilisateur(self,nom,prenom):
        if not all([nom,prenom]):
            raise ValueError("Veuillez indiques le nom et le prenom de l'utilisateur")

        id=self.utilisateurs.user_id(nom,prenom)

        if not id:
            raise ValueError("Utilisateur inexistant !")
        return id
    
    def afficher(self,id):
        if not id:
            raise ValueError("Veuilles indiques l'identifiant de l'utilisateur")
        return  self.utilisateurs.user_search(id)

class Borrow_Manager:
    def __init__(self,bd):
           self.bd=bd
           self.emprunt=EMPRUNT(self.bd)
           self.utilisateur=Utilisateurs(self.bd)
           self.book=Livre(self.bd)
    
    def ajout_un_emprunt(self,id_user,id_book):

        if not all([id_book,id_user]):
            raise ValueError("Veuillez indiquez les identifiants de l'utilisateur et du livre")
        
        date_emprunt= date.today()
        date_retour_prevue = date_emprunt + timedelta(days=14) 

        if not self.utilisateur.user_search(id_user):
            raise ValueError("Cet Utilisateur n'existe pas")
        
        nbre=self.book.search_book(id_book)
        if not nbre:
            raise ValueError ("Ce Livre n'existe pas !")
        
        exemplaire=nbre[5]
        if  exemplaire == 0:
            raise ValueError("cet Emprunt ne peut etre effectue car le nombre d'exemplaire du livre est epuise")
        
        cota=self.emprunt.nbre_livre_emprunter_Par_un_utilisateur(id_user)

        if cota > 2 :
            raise ValueError("Cet utilisateur a atteint sa limite d'emprunt")
        already=self.emprunt.livre_deja_emprunter(id_book,id_user)
        if already:
            raise ValueError("Attention,Vous ne pouvez pas emprunter deux fois le meme livre")
        
        retard=self.emprunt.a_des_retard(id_user)
        if  retard is not None and retard>0:
            raise ValueError("cet utilisateur a deja un emprunt en retard,et ne peut emprunter a nouveau")
        
        emprunt = self.emprunt.ajouter_emprunt(id_user,id_book,date_emprunt,date_retour_prevue)

        if emprunt == 0:
            return False
        else:
            return True

    def cota_emprunt(self,id_user):
        if not id_user:
            raise ValueError ("Veuillez indiquez l'identifiant de l'utilisateur ")
        if not self.utilisateur.user_search(id_user):
            raise ValueError("Cet Utilisateur n'existe pas")
        
        cota=self.emprunt.nbre_livre_emprunter_Par_un_utilisateur(id_user)
        return cota
    
    def historique_emprunt(self,id_user):
        if not id_user:
          raise ValueError ("Veuillez indiquez l'identifiant de l'utilisateur ")
        if not self.utilisateur.user_search(id_user):
            raise ValueError("Cet Utilisateur n'existe pas")
        historique=self.emprunt.historique_emprunts_utilisateur(id_user)
        if not historique:
            return False #cet utilisateur n'a jamais emprunter de livre

        return historique
    
    def emprunt_en_cours(self,id_user):
        if not id_user:
          raise ValueError ("Veuillez indiquez l' identifiant de l'utilisateur ")
        if not self.utilisateur.user_search(id_user):
            raise ValueError("Cet Utilisateur n'existe pas")
        current=self.emprunt.emprunts_encours(id_user)
        if not current:
            return False #cet utilise ne possede aucun livre actuellement

        return current
    
    def retourner_emprunt(self,id_book,id_user):
        if not all([id_book,id_user]):
            raise ValueError("Veuillez indiquez les identifiants de l'utilisateur et du livre")
        modif,retard=self.emprunt.valider_retour(id_book,id_user)
        if not modif or modif == 0:
            raise ValueError("Ce livre n'est pas enregistré comme emprunté par cet utilisateur.")
        nbre_jours=int(retard) if retard is not None else 0

        en_retard={"status":"retourne","retard":nbre_jours}
        en_avance={"status":"retourne","Avance":abs(nbre_jours)}
        a_jour={"status":"retourne","Jour-j":0}
    
        if nbre_jours>0:
           return en_retard
        elif nbre_jours <0 :
            return en_avance
        else :
            return a_jour
        
    def afficher_les_emprunts(self):
        emprunts=self.emprunt.afficher_emprunts()

        return emprunts

    
    
        

        
      
        
        

    

    

 





 