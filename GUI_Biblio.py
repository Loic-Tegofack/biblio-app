import tkinter as tk
from tkinter import ttk,messagebox
from controleurBiblio import Book_Manager,Author_Manager

root=tk.Tk()
root.title("BIBLIO 1.0")
root.geometry("700x500")
livres=Book_Manager("pop.db")
Auteur=Author_Manager("pop.db")


class GUI:
    def __init__(self):

        self.ajout=None
   
        self.afficher_formulaire()

        self.creer_tableau()

        self.afficher_livre()

        self.creer_menu()   

    def formulaire_ajout_livre(self):

       self.ajout=tk.Frame(root)
       self.ajout.pack()
       self.ajout.grab_set()
       self.ajouter_btn.config(state="disabled")#desactive le bouton une fois qu'on a cliquer

       tk.Label(self.ajout,text="Titre:").grid(row=0,column=0)
       self.titre_livre=tk.Entry(self.ajout)
       self.titre_livre.grid(row=0,column=1)
      
         
       tk.Label(self.ajout,text="Auteur").grid(row=0,column=2,padx=10)
       self.auteur_livre=tk.Entry(self.ajout)
       self.auteur_livre.grid(row=0,column=3)

       tk.Label(self.ajout,text="Annee de publication : ").grid(row=1,column=0)
       self.date_livre=tk.Entry(self.ajout)
       self.date_livre.grid(row=1,column=1)

       tk.Label(self.ajout,text="Genre:").grid(row=2,column=0)
       self.genre_livre=tk.Entry(self.ajout)
       self.genre_livre.grid(row=2,column=1)

       tk.Label(self.ajout,text="Quantite:").grid(row=3,column=0)
       self.qte=tk.Entry(self.ajout)
       self.qte.grid(row=3,column=1)

       tk.Label(self.ajout,text="Etat:").grid(row=4,column=0)
       self.state=tk.Entry(self.ajout)
       self.state.grid(row=4,column=1)

       self.btn_ajout=tk.Button(self.ajout,text="AJOUTER",command=self.validation_ajout_livre).grid(row=6,column=2,pady=15,padx=15)
       self.btn_annuler=tk.Button(self.ajout,text="Annuler",command=self.fermer_formulaire).grid(row=6,column=3,pady=15,padx=15)
     
    def ajout_auteur(self,nom):
       self.auteur=tk.Toplevel(self.ajout)
       self.auteur.title("Ajout Auteur Inexistant !")
       self.auteur.geometry("200x150")
       self.auteur.grab_set()


       tk.Label(self.auteur,text="Auteur").grid(row=0,column=0,padx=10)
       author=tk.Entry(self.auteur)
       author.insert(0,self.auteur_livre.get())
       author.config(state="readonly")
       author.grid(row=0,column=1)

       tk.Label(self.auteur,text="Date Naissance:").grid(row=1,column=0)
       self.date_auteur=tk.Entry(self.auteur)
       self.date_auteur.grid(row=1,column=1)

       tk.Label(self.auteur,text="Pays").grid(row=2,column=0)
       self.auteur_pays=tk.Entry(self.auteur)
       self.auteur_pays.grid(row=2,column=1)

       resultat=None

       def validation_auteur():
            date=self.date_auteur.get().strip()
            pays=self.auteur_pays.get().strip()

            nonlocal resultat

            date_auteur_int=0
            if date.isdigit() :
                date_auteur_int=int(date) 
            else:
                messagebox.showwarning("Attention!","l'annee de naissance de l'auteur doit etre un nombre positif !",parent=self.auteur)
                return 
            try:
              Auteur.get_or_create_auteur(nom,date_auteur_int,pays)
              resultat=True
              self.auteur.destroy()
            except Exception as e:
                messagebox.showerror("Erreur !",f"{e}",parent=self.auteur)
                resultat=None

       tk.Button(self.auteur,text="Ajouter",command=validation_auteur).grid(row=3, column=0, pady=12)
       tk.Button(self.auteur,text="Annuler",command=self.auteur.destroy).grid(row=3, column=1, pady=12)
    
       self.auteur.wait_window() #bloque la fenetre auteur jusqu'a ce que l'utilisateur ai fourni les infos ou l'ai fermer.
       return resultat

    def validation_ajout_livre(self):
        nom=self.auteur_livre.get()
        titre_book=self.titre_livre.get()
        date=self.date_livre.get()
        etat_book=self.state.get()
        qtes=self.qte.get()
        cat=self.genre_livre.get()
       
        date_livre_int=0
        qt=0

        if not all([nom,titre_book,date,etat_book,qtes,cat]):
            messagebox.showwarning("Champs Vide!","Un ou plusieurs champs sont vides ! \n Veuillez les remplir !!")
            return

        if date.isdigit():
            date_livre_int=int(date)
        else:
            messagebox.showwarning("Incoherence donnee!","l'annee de publication du livre doit etre un nombre positif !")
            return
        if qtes.isdigit():
            qt=int(qtes)
        else:
            messagebox.showwarning("Incoherence donnee!","le nombre d'exemplaire du livre doit etre un nombre positif !")
            return
        
        if Auteur.recherche(nom) is None :
            reponse=messagebox.askyesno("Auteur Inconnu !",f"{nom} n'est pas enregistrer !, souhaitez-vous l'ajouter ?")
            if reponse:
                if self.ajout_auteur(nom) is None:
                    messagebox.showwarning("Action impossible !","Vous ne pouvez ajouter un livre sans auteur !")
                    return
            else:
                messagebox.showwarning("Action impossible !","Vous ne pouvez ajouter un livre sans auteur !")
                return
            
        try:
            resultat=livres.ajouter_livre(titre_book,nom,None,None,etat_book,date_livre_int,qt,cat)
            if resultat is True:
               messagebox.showinfo("infos",f"Le livre {titre_book} a bien ete ajouter !")
               self.afficher_livre()
               self.effacer_champs()
            else:
                messagebox.showinfo("Redondance",f"{titre_book} existe deja")

        except Exception as e :
              messagebox.showerror("Erreur!",str(e))

    def effacer_champs(self):
          for champ in [self.auteur_livre,self.titre_livre,self.date_livre,self.state,self.qte,self.genre_livre]:
              champ.delete(0,tk.END)

    def afficher_formulaire(self):
        self.ajouter_btn=tk.Button(root,text="Ajouter Un Livre",command=self.formulaire_ajout_livre)
        self.ajouter_btn.pack()
    def fermer_formulaire(self):
        if self.ajout is not None :
            self.ajout.destroy()
            self.ajout=None
            self.ajouter_btn.config(state="normal")


    #Nouvelle Approche (sur le Treeview): clic-droit -> menu -> [afficher details-(ou)-modifier-(ou)-supprimer] -> choisir -> valider
     
    def creer_menu(self):
        #on creer le menu
        self.menu=tk.Menu(root,tearoff=0)

        self.menu.add_command(label="Afficher Details",command=self.afficher_detail_menu)

        self.menu.add_separator()
        
        self.menu.add_command(label="Modifier un Livre",command=self.details_modification)

        self.menu.add_separator()

        self.menu.add_command(label="Supprimer un livre",command=self.supprimer_livre)

        self.tableau.bind("<Button-3>",self.afficher_menu_contextuel) # on lie notre menu au treeview
    
    def afficher_menu_contextuel(self,event):
        #on affiche le menu lorsqu'une ligne est selectionnee
        ligne=self.tableau.identify_row(event.y)

        if ligne:
            self.tableau.selection_set(ligne) #indique visuelement ligne selectionne
            self.menu.post(event.x_root,event.y_root) # cette methode (post) permet de situer le menu a l'endroit exact du clic/selection
        #x et y etant les coordonne de la ligne selectionne
    
    def afficher_detail_menu(self):
        selection=self.tableau.selection()#recupere l'id de la ligne selectionner et renvoie un tuple
        if not selection:
            return
        id=selection[0]
        id_livre=self.tableau.item(id,"tags")[0]
        self.afficher_details(livre_id=int(id_livre),mode=False)
    def details_modification(self):
        selection=self.tableau.selection()
        if not selection:
            return
        id=selection[0]
        id_livre=self.tableau.item(id,"tags")[0]
        self.afficher_details(livre_id=int(id_livre),mode=True)
    
    def supprimer_livre(self):
        selection=self.tableau.selection()
        if not selection:
            return
        id=selection[0]
        id_livre=self.tableau.item(id,"tags")[0]

        info=livres.recherche_par_id(int(id_livre))
        question=messagebox.askyesno("suppression ..action irreversiverble",f"Supprimer ce Livre ? \n\n" 
                            f"Titre: {info[1]} \n"
                            f"Auteur:{info[0]}\n"
                            f" Genre:{info[3]} \n"
                            f"Date:{info[2]}\n\n"
                            f"Cette action est Irreversible !")
        if not question:
            return
        try:
            livres.supprimer_livre(info[1])
            messagebox.showinfo("infos",f"le livre {info[1]} a bien ete supprimer")
            self.afficher_livre()
        except Exception as e:
                messagebox.showerror("erreur",str(e))
        
                        

    def creer_tableau(self):
        conteneur=tk.Frame(root)
        conteneur.pack(fill="both",expand=True,anchor="s")

        colonne=("auteur","titre","genre","etat")
        self.tableau=ttk.Treeview(conteneur,columns=colonne,show="headings")
        self.tableau.bind("<Double-1>",self.afficher_details)

        scroll=tk.Scrollbar(conteneur,orient="vertical",command=self.tableau.yview)
        self.tableau.configure(yscrollcommand=scroll.set)

        self.tableau.heading("auteur",text="Auteur")
        self.tableau.heading("titre",text="Titre")
        self.tableau.heading("genre",text="Genre")

        self.tableau.heading("etat",text="Etat")

        self.tableau.column("auteur",width=120)
        self.tableau.column("titre",width=250)
        self.tableau.column("genre",width=150)
        self.tableau.column("etat",width=150)

        self.tableau.pack(side="left", fill="x", expand=True)
        scroll.pack(side="right", fill="y")
       

    def afficher_livre(self):
       #On  vide le tableau avant de le remplir
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        Livres=livres.afficher_livre()
        print(f"Nombre de livres récupérés : {len(Livres)}")  # ← DEBUG
        print(f"Livres : {Livres}")  # ← DEBUG

        for livre in Livres :
            self.tableau.insert("","end",values=(livre[1],livre[2],livre[4],livre[5]),tags=(livre[0],))
#ici tags nous permet de  recuperer l'identifiant des livres et a les rendre invisible par l'utilisateur
    
    def afficher_details(self,event=None,livre_id=None,mode=None):

        if event:
            selection=self.tableau.selection()#on recupere l'identifiant de la ligne selectionner(il apparait sous forme de tuples)
            if not selection:
                return
            item=selection[0] #si plusieur lignes selectionnees,on recupere l'id de la premiere ligne 
            livre_id=self.tableau.item(item,"tags")[0]# on recupere l'id cache du/des livre(s) 

        if livre_id is None:
            return
          
        self.id=int(livre_id)
        info_livres=livres.recherche_par_id(self.id)

        self.details=tk.Toplevel(root)
        self.details.title(f"Details :{info_livres[1]}")
        self.details.geometry("550x200")
        self.details.grab_set()

        self.dict={
                "titre":info_livres[1],
                "date":info_livres[2],
                "genre":info_livres[3],
                "etat":info_livres[4],
                "stock":info_livres[5]
            }
        
        tk.Label(self.details,text="Titre:",font=("Arial",10,"bold")).grid(row=0,column=0,padx=5,pady=5)
        self.titre=tk.StringVar(value=info_livres[1])
        self.val_titre=tk.Entry(self.details,textvariable=self.titre,state="readonly")
        self.val_titre.grid(row=0,column=1,padx=5,pady=5)

        tk.Label(self.details,text="Auteur :",font=("Arial",10,"bold")).grid(row=0,column=2,padx=5,pady=5)
        self.auteur=tk.StringVar(value=info_livres[0])
        self.val_auteur=tk.Entry(self.details,textvariable=self.auteur,state="readonly")
        self.val_auteur.grid(row=0,column=3,padx=5,pady=5)

        tk.Label(self.details,text="Date-Publication :",font=("Arial",10,"bold")).grid(row=1,column=0,padx=5,pady=5)
        self.date=tk.StringVar(value=info_livres[2])
        self.val_date=tk.Entry(self.details,textvariable=self.date,state="readonly")
        self.val_date.grid(row=1,column=1,padx=5,pady=5)

        tk.Label(self.details,text="Genre Litteraire:",font=("Arial",10,"bold")).grid(row=1,column=2,padx=5,pady=5)
        self.genre=tk.StringVar(value=info_livres[3])
        self.val_genre=tk.Entry(self.details,textvariable=self.genre,state="readonly")
        self.val_genre.grid(row=1,column=3,padx=5,pady=5)

        tk.Label(self.details,text="Etat:",font=("Arial",10,"bold")).grid(row=2,column=0,padx=5,pady=5)
        self.etat=tk.StringVar(value=info_livres[4])
        self.val_etat=tk.Entry(self.details,textvariable=self.etat,state="readonly")
        self.val_etat.grid(row=2,column=1,padx=5,pady=5)

        tk.Label(self.details,text="Stocks:",font=("Arial",10,"bold")).grid(row=2,column=2,padx=5,pady=5)
        self.stock=tk.StringVar(value=info_livres[5])
        self.val_stock=tk.Entry(self.details,textvariable=self.stock,state="readonly")
        self.val_stock.grid(row=2,column=3,padx=5,pady=5)

        if mode:
            self.modifier=tk.Button(self.details,text="Modifier",command=self.modifier_livre)
            self.modifier.grid(row=4,column=0,padx=15,pady=15)

        
    def modifier_livre(self):
        self.modifier.grid_remove()
        self.details.title(f"Modification ! {self.titre.get()} ")
        self.saisi=[self.val_date,self.val_etat,self.val_genre,self.val_stock,self.val_titre]
        
        for champ in self.saisi:
            champ.config(state="normal") 


        self.annuler=tk.Button(self.details,text="Annuler",command=self.annuler_modifcation)
        self.annuler.grid(row=3,column=0,padx=15,pady=15)
        self.sauvegarde=tk.Button(self.details,text="Sauvegarder",command=self.sauvegarder_modification)
        self.sauvegarde.grid(row=3,column=1,padx=15,pady=15)
    
    def sauvegarder_modification(self):
       stock=self.stock.get()
       date=self.date.get()
       if stock.isdigit() and date.isdigit():
            stock_int=int(self.stock.get())
            date_int=int(self.date.get())
       else:
            messagebox.showwarning("Attention!","la quantite de livre et la date doivent etre des nombres positifs !")
            return
       dict_actuelle={
           
             "titre":self.titre.get(),
             "date":int(self.date.get()),
             "genre":self.genre.get(),
             "etat":self.etat.get(),
             "stock":int(self.stock.get())
        }
   

       if self.dict == dict_actuelle:
           messagebox.showinfo("RAS","Aucune modification apporter !")
           return
       if not all ([self.titre.get(),self.date.get(),self.genre.get(),self.etat.get(),self.stock.get()] ):
           messagebox.showwarning("Attention !","Un ou plusieurs champs sont  vide ! veuillez tous les renseigner !")
           return

       if  messagebox.askyesno("Attention !","Voulez-vous enregistrer les changements apportee ?") :
           livres.modifier_livre(self.id,self.titre.get(),date_int,self.genre.get(),self.etat.get(),stock_int)
           messagebox.showinfo("infos",f"le livre {self.titre.get()} a ete modifier !")
           self.dict=dict_actuelle
           self.details.destroy()
           self.afficher_livre()
       else:
           self.annuler_modifcation()
            
    
    def annuler_modifcation(self):
        self.details.title("Initiale !")
        self.sauvegarde.grid_forget()
        self.annuler.grid_forget()
        self.modifier.grid()
        
        self.titre.set(self.dict["titre"])
        self.date.set(self.dict["date"])
        self.etat.set(self.dict["etat"])
        self.genre.set(self.dict["genre"])
        self.stock.set(self.dict["stock"])

        for champ in self.saisi:
            champ.config(state="readonly")


app =GUI()


root.mainloop()