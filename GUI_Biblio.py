import customtkinter as ctk
from tkinter import ttk, messagebox
from controleurBiblio import Book_Manager, Author_Manager, User_Manager, Borrow_Manager

# Configuration CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Instances globales
livres = Book_Manager("test.db")
auteur = Author_Manager("test.db")
utilisateur = User_Manager("test.db")
emprunt = Borrow_Manager("test.db")


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Biblio - Gestion de Bibliothèque")
        self.root.geometry("1400x850")

        self.tabview = ctk.CTkTabview(self.root, corner_radius=15)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tabview.add("📚 Livres")
        self.tabview.add("✍️ Auteurs")
        self.tabview.add("👤 Utilisateurs")
        self.tabview.add("📋 Emprunts")

        self.gui_livre   = Livres_GUI(self.tabview.tab("📚 Livres"))
        self.gui_auteur  = Auteur_GUI(self.tabview.tab("✍️ Auteurs"))
        self.gui_user    = USER_GUI(self.tabview.tab("👤 Utilisateurs"))
        self.gui_emprunt = Emprunt_GUI(self.tabview.tab("📋 Emprunts"))


# ─────────────────────────────────────────────────────────────────────────────
#  HELPER
# ─────────────────────────────────────────────────────────────────────────────
def bind_close_reactivate(window, button):
    """Intercepte la croix rouge et réactive le bouton associé."""
    def _on_close():
        window.destroy()
        if button and button.winfo_exists():
            button.configure(state="normal")
    window.protocol("WM_DELETE_WINDOW", _on_close)


# =============================================================================
#  LIVRES
# =============================================================================
class Livres_GUI:
    def __init__(self, parent):
        self.parent = parent
        self.ajout  = None

        header = ctk.CTkFrame(self.parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(10, 0))

        self.ajouter_btn = ctk.CTkButton(
            header, text="+ Nouveau livre",
            command=self.formulaire_ajout_livre,
            width=160, height=40, corner_radius=10,
            font=("Segoe UI", 13, "bold")
        )
        self.ajouter_btn.pack(side="left", padx=(0, 10))

        search_frame = ctk.CTkFrame(header, fg_color="transparent")
        search_frame.pack(side="left", fill="x", expand=True)

        self.cherche = ctk.CTkEntry(
            search_frame, placeholder_text="🔍 Rechercher un livre...",
            width=300, height=40, corner_radius=10, font=("Segoe UI", 12)
        )
        self.cherche.pack(side="left", padx=(0, 10))

        ctk.CTkButton(search_frame, text="Rechercher", command=self.afficher_recherche,
            width=130, height=40, corner_radius=10,
            fg_color="#2196F3", hover_color="#1976D2").pack(side="left", padx=(0, 10))

        ctk.CTkButton(search_frame, text="Afficher tout", command=self.afficher_livre,
            width=130, height=40, corner_radius=10,
            fg_color="gray40", hover_color="gray30").pack(side="left")

        self.creer_tableau()
        self.afficher_livre()
        self.creer_menu()

    # ── Formulaire ajout livre ─────────────────────────────────────────────
    def formulaire_ajout_livre(self):
        self.ajout = ctk.CTkToplevel(self.parent)
        self.ajout.title("Nouveau livre")
        self.ajout.geometry("700x650")
        self.ajout.resizable(False, False)
        self.ajout.grab_set()
        self.ajouter_btn.configure(state="disabled")
        bind_close_reactivate(self.ajout, self.ajouter_btn)

        main_frame = ctk.CTkFrame(self.ajout, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(main_frame, text="📖 Ajouter un nouveau livre",
            font=("Segoe UI", 24, "bold")).pack(pady=(0, 30))

        ff = ctk.CTkFrame(main_frame, fg_color="transparent")
        ff.pack(fill="both", expand=True)

        ctk.CTkLabel(ff, text="Titre *",        font=("Segoe UI", 13, "bold"), text_color="#d32f2f").grid(row=0, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.titre_livre = ctk.CTkEntry(ff, width=280, height=40, corner_radius=8)
        self.titre_livre.grid(row=1, column=0, pady=(0, 20), padx=(0, 15))

        ctk.CTkLabel(ff, text="Nom auteur *",   font=("Segoe UI", 13, "bold"), text_color="#d32f2f").grid(row=0, column=1, sticky="w", pady=(0, 8))
        self.auteur_nom_livre = ctk.CTkEntry(ff, width=280, height=40, corner_radius=8)
        self.auteur_nom_livre.grid(row=1, column=1, pady=(0, 20))

        ctk.CTkLabel(ff, text="Prénom auteur *",font=("Segoe UI", 13, "bold"), text_color="#d32f2f").grid(row=2, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.auteur_prenom_livre = ctk.CTkEntry(ff, width=280, height=40, corner_radius=8)
        self.auteur_prenom_livre.grid(row=3, column=0, pady=(0, 20), padx=(0, 15))

        ctk.CTkLabel(ff, text="Année",          font=("Segoe UI", 12), text_color="gray50").grid(row=2, column=1, sticky="w", pady=(0, 8))
        self.date_livre = ctk.CTkEntry(ff, width=280, height=40, corner_radius=8)
        self.date_livre.grid(row=3, column=1, pady=(0, 20))

        ctk.CTkLabel(ff, text="Genre",          font=("Segoe UI", 12), text_color="gray50").grid(row=4, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.genre_livre = ctk.CTkEntry(ff, width=280, height=40, corner_radius=8)
        self.genre_livre.grid(row=5, column=0, pady=(0, 20), padx=(0, 15))

        ctk.CTkLabel(ff, text="Quantité",       font=("Segoe UI", 12), text_color="gray50").grid(row=4, column=1, sticky="w", pady=(0, 8))
        self.qte = ctk.CTkEntry(ff, width=280, height=40, corner_radius=8)
        self.qte.grid(row=5, column=1, pady=(0, 20))

        ctk.CTkLabel(ff, text="État *",         font=("Segoe UI", 13, "bold"), text_color="#d32f2f").grid(row=6, column=0, sticky="w", pady=(0, 8), padx=(0, 10))
        self.state = ctk.CTkEntry(ff, width=280, height=40, corner_radius=8)
        self.state.grid(row=7, column=0, pady=(0, 20), padx=(0, 15))

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=(10, 0))

        ctk.CTkButton(btn_frame, text="✓ Ajouter", command=self.validation_ajout_livre,
            width=180, height=45, corner_radius=10,
            font=("Segoe UI", 14, "bold"), fg_color="#4CAF50", hover_color="#45a049").pack(side="left", padx=8)

        ctk.CTkButton(btn_frame, text="✕ Annuler", command=self.fermer_formulaire,
            width=180, height=45, corner_radius=10,
            font=("Segoe UI", 14, "bold"), fg_color="gray40", hover_color="gray30").pack(side="left", padx=8)

    def ajout_auteur_popup(self, nom, prenom):
        self.auteur_window = ctk.CTkToplevel(self.ajout)
        self.auteur_window.title("Auteur inexistant")
        self.auteur_window.geometry("450x300")
        self.auteur_window.grab_set()

        main = ctk.CTkFrame(self.auteur_window, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(main, text="⚠️ Auteur non trouvé", font=("Segoe UI", 18, "bold")).pack(pady=(0, 20))
        ctk.CTkLabel(main, text=f"Auteur : {nom} {prenom}", font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(main, text="Année de naissance", font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 5))
        self.date_auteur = ctk.CTkEntry(main, width=350, height=35, corner_radius=8)
        self.date_auteur.pack(pady=(0, 15))

        ctk.CTkLabel(main, text="Pays", font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 5))
        self.auteur_pays = ctk.CTkEntry(main, width=350, height=35, corner_radius=8)
        self.auteur_pays.pack(pady=(0, 20))

        resultat = [None]

        def validation_auteur():
            try:
                auteur.get_or_create_auteur(nom, prenom,
                    self.date_auteur.get().strip(),
                    self.auteur_pays.get().strip())
                resultat[0] = True
                self.auteur_window.destroy()
            except Exception as e:
                messagebox.showwarning("Attention!", str(e), parent=self.auteur_window)

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(10, 0))
        ctk.CTkButton(btn_frame, text="Ajouter", command=validation_auteur, width=150, height=40, corner_radius=8).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Annuler", command=self.auteur_window.destroy, width=150, height=40, corner_radius=8, fg_color="gray40").pack(side="left", padx=5)

        self.auteur_window.wait_window()
        return resultat[0]

    def validation_ajout_livre(self):
        nom        = self.auteur_nom_livre.get().strip()
        prenom     = self.auteur_prenom_livre.get().strip()
        titre_book = self.titre_livre.get().strip()
        date       = self.date_livre.get().strip()
        etat_book  = self.state.get().strip()
        qtes       = self.qte.get().strip()
        cat        = self.genre_livre.get().strip()

        if not all([nom, prenom, titre_book, etat_book]):
            messagebox.showwarning("Champs vides !", "Le titre, nom/prénom auteur et l'état sont requis !")
            return

        if auteur.retourne_id_auteur(nom, prenom) is None:
            if messagebox.askyesno("Auteur inconnu", f"{nom} {prenom} n'est pas enregistré. L'ajouter ?"):
                if self.ajout_auteur_popup(nom, prenom) is None:
                    return
            else:
                return

        try:
            resultat = livres.ajouter_livre(
                titre_book, nom, prenom, None, None,
                etat_book, date or None, qtes or None, cat or None
            )
            if resultat:
                messagebox.showinfo("Succès !", f"✓ Le livre '{titre_book}' a été ajouté !")
                self.afficher_livre()
                self.fermer_formulaire()
        except Exception as e:
            messagebox.showerror("Erreur !", str(e))

    def fermer_formulaire(self):
        if self.ajout and self.ajout.winfo_exists():
            self.ajout.destroy()
            self.ajout = None
        if self.ajouter_btn.winfo_exists():
            self.ajouter_btn.configure(state="normal")

    # ── Tableau ────────────────────────────────────────────────────────────
    def creer_tableau(self):
        tree_frame = ctk.CTkFrame(self.parent, corner_radius=10)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(15, 20))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
            background="#ffffff", foreground="#2b2b2b",
            fieldbackground="#ffffff", borderwidth=0,
            font=("Segoe UI", 11), rowheight=32)
        style.configure("Treeview.Heading",
            background="#1976D2", foreground="white",
            font=("Segoe UI", 12, "bold"), borderwidth=0)
        style.map("Treeview",
            background=[("selected", "#2196F3")],
            foreground=[("selected", "white")])

        colonne = ("auteur", "titre", "genre", "etat")
        self.tableau = ttk.Treeview(tree_frame, columns=colonne, show="headings")
        self.tableau.heading("auteur", text="📝 Auteur")
        self.tableau.heading("titre",  text="📖 Titre")
        self.tableau.heading("genre",  text="🎭 Genre")
        self.tableau.heading("etat",   text="📊 État")
        self.tableau.column("auteur", width=250)
        self.tableau.column("titre",  width=350)
        self.tableau.column("genre",  width=200)
        self.tableau.column("etat",   width=150)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tableau.yview)
        self.tableau.configure(yscrollcommand=scrollbar.set)
        self.tableau.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y")
        self.tableau.bind("<Double-1>", self.afficher_details)

    def creer_menu(self):
        import tkinter as tk
        self.menu = tk.Menu(self.parent, tearoff=0)
        self.menu.add_command(label="👁️ Afficher détails", command=self.afficher_detail_menu)
        self.menu.add_separator()
        self.menu.add_command(label="✏️ Modifier",  command=self.details_modification)
        self.menu.add_separator()
        self.menu.add_command(label="🗑️ Supprimer", command=self.supprimer_livre)
        self.tableau.bind("<Button-3>", self.afficher_menu_contextuel)

    def afficher_menu_contextuel(self, event):
        ligne = self.tableau.identify_row(event.y)
        if ligne:
            self.tableau.selection_set(ligne)
            self.menu.post(event.x_root, event.y_root)

    def afficher_detail_menu(self):
        selection = self.tableau.selection()
        if not selection:
            return
        id_livre = self.tableau.item(selection[0], "tags")[0]
        self.afficher_details(livre_id=int(id_livre), mode=False)

    def details_modification(self):
        selection = self.tableau.selection()
        if not selection:
            return
        id_livre = self.tableau.item(selection[0], "tags")[0]
        self.afficher_details(livre_id=int(id_livre), mode=True)

    def supprimer_livre(self):
        selection = self.tableau.selection()
        if not selection:
            return
        id_livre = self.tableau.item(selection[0], "tags")[0]
        info = livres.recherche_par_id(int(id_livre))
        # info → (nom_auteur, prenom_auteur, titre, date, genre, etat, nbre_exemplaire)
        if messagebox.askyesno("Confirmation", f"Supprimer '{info[2]}' ?\n\nCette action est irréversible !"):
            try:
                livres.supprimer_livre(info[2])
                messagebox.showinfo("Succès", f"✓ '{info[2]}' supprimé !")
                self.afficher_livre()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def afficher_recherche(self):
        result = self.cherche.get().strip()
        if not result:
            messagebox.showinfo("Champ vide", "Veuillez saisir un titre !")
            return
        livre = livres.rechercher(result)
        if not livre:
            messagebox.showinfo("Non trouvé", f"'{result}' n'existe pas !")
            return
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        id_book = livres.book_id(result)
        # search_book → (nom_auteur, prenom_auteur, titre, date, genre, etat, nbre_exemplaire)
        self.tableau.insert("", "end",
            values=(f"{livre[0]} {livre[1]}", livre[2], livre[4], livre[5]),
            tags=(id_book,))

    def afficher_livre(self):
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        # display_book → (id, nom_auteur, prenom_auteur, titre, date, genre, etat, nbre_exemplaire)
        for l in livres.afficher_livre():
            self.tableau.insert("", "end",
                values=(f"{l[1]} {l[2]}", l[3], l[5], l[6]),
                tags=(l[0],))

    # ── Détails / Modification livre ───────────────────────────────────────
    def afficher_details(self, event=None, livre_id=None, mode=None):
        if event:
            selection = self.tableau.selection()
            if not selection:
                return
            livre_id = self.tableau.item(selection[0], "tags")[0]
        if livre_id is None:
            return

        self.id  = int(livre_id)
        info = livres.recherche_par_id(self.id)
        # info → (nom_auteur, prenom_auteur, titre, date, genre, etat, nbre_exemplaire)

        import tkinter as tk
        self.details = tk.Toplevel(self.parent)
        self.details.title(f"Détails : {info[2]}")
        self.details.geometry("650x280")
        self.details.grab_set()

        self.dict = {"titre": info[2], "date": info[3], "genre": info[4], "etat": info[5], "stock": info[6]}

        tk.Label(self.details, text="Titre:",  font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.titre = tk.StringVar(value=info[2])
        self.val_titre = tk.Entry(self.details, textvariable=self.titre, state="readonly", font=("Segoe UI", 10), width=20)
        self.val_titre.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.details, text="Auteur:", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=10, pady=10, sticky="e")
        tk.Entry(self.details, textvariable=tk.StringVar(value=f"{info[0]} {info[1]}"), state="readonly", font=("Segoe UI", 10), width=20).grid(row=0, column=3, padx=10, pady=10)

        tk.Label(self.details, text="Date:",   font=("Segoe UI", 10, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.date = tk.StringVar(value=info[3])
        self.val_date = tk.Entry(self.details, textvariable=self.date, state="readonly", font=("Segoe UI", 10), width=20)
        self.val_date.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.details, text="Genre:",  font=("Segoe UI", 10, "bold")).grid(row=1, column=2, padx=10, pady=10, sticky="e")
        self.genre = tk.StringVar(value=info[4])
        self.val_genre = tk.Entry(self.details, textvariable=self.genre, state="readonly", font=("Segoe UI", 10), width=20)
        self.val_genre.grid(row=1, column=3, padx=10, pady=10)

        tk.Label(self.details, text="État:",   font=("Segoe UI", 10, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.etat = tk.StringVar(value=info[5])
        self.val_etat = tk.Entry(self.details, textvariable=self.etat, state="readonly", font=("Segoe UI", 10), width=20)
        self.val_etat.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.details, text="Stock:",  font=("Segoe UI", 10, "bold")).grid(row=2, column=2, padx=10, pady=10, sticky="e")
        self.stock = tk.StringVar(value=info[6])
        self.val_stock = tk.Entry(self.details, textvariable=self.stock, state="readonly", font=("Segoe UI", 10), width=20)
        self.val_stock.grid(row=2, column=3, padx=10, pady=10)

        if mode:
            tk.Button(self.details, text="✏️ Modifier", command=self.modifier_livre,
                bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold"), width=12).grid(row=4, column=1, pady=15)

    def modifier_livre(self):
        self.saisi = [self.val_date, self.val_etat, self.val_genre, self.val_stock, self.val_titre]
        for champ in self.saisi:
            champ.config(state="normal")
        import tkinter as tk
        tk.Button(self.details, text="💾 Sauvegarder", command=self.sauvegarder_modification,
            bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"), width=12).grid(row=4, column=1, pady=15)
        tk.Button(self.details, text="✕ Annuler", command=self.annuler_modifcation,
            bg="gray", fg="white", font=("Segoe UI", 10, "bold"), width=12).grid(row=4, column=2, pady=15)

    def sauvegarder_modification(self):
        stock = self.stock.get()
        date  = self.date.get()
        if not (stock.isdigit() and date.isdigit()):
            messagebox.showwarning("Attention!", "La quantité et la date doivent être des nombres !")
            return
        dict_actuelle = {"titre": self.titre.get(), "date": int(date), "genre": self.genre.get(), "etat": self.etat.get(), "stock": int(stock)}
        if self.dict == dict_actuelle:
            messagebox.showinfo("Aucun changement", "Aucune modification détectée !")
            return
        if messagebox.askyesno("Confirmation", "Enregistrer les modifications ?"):
            livres.modifier_livre(self.id, self.titre.get(), int(date), self.genre.get(), self.etat.get(), int(stock))
            messagebox.showinfo("Succès", f"✓ '{self.titre.get()}' modifié !")
            self.details.destroy()
            self.afficher_livre()

    def annuler_modifcation(self):
        self.titre.set(self.dict["titre"])
        self.date.set(self.dict["date"])
        self.etat.set(self.dict["etat"])
        self.genre.set(self.dict["genre"])
        self.stock.set(self.dict["stock"])
        for champ in self.saisi:
            champ.config(state="readonly")
        self.details.destroy()


# =============================================================================
#  AUTEURS
# =============================================================================
class Auteur_GUI:
    def __init__(self, parent):
        self.parent = parent

        # Header avec bouton + barre de recherche
        header = ctk.CTkFrame(self.parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        self.bt = ctk.CTkButton(
            header, text="+ Nouvel auteur",
            command=self.ajouter_auteur,
            width=160, height=40, corner_radius=10,
            font=("Segoe UI", 13, "bold")
        )
        self.bt.pack(side="left", padx=(0, 20))

        self.cherche_nom    = ctk.CTkEntry(header, placeholder_text="Nom",    width=160, height=40, corner_radius=8)
        self.cherche_nom.pack(side="left", padx=(0, 8))

        self.cherche_prenom = ctk.CTkEntry(header, placeholder_text="Prénom", width=160, height=40, corner_radius=8)
        self.cherche_prenom.pack(side="left", padx=(0, 8))

        ctk.CTkButton(header, text="🔍 Rechercher", command=self.rechercher_auteur,
            width=130, height=40, corner_radius=8,
            fg_color="#2196F3", hover_color="#1976D2").pack(side="left", padx=(0, 8))

        ctk.CTkButton(header, text="Afficher tout", command=self.affichage_auteur,
            width=120, height=40, corner_radius=8,
            fg_color="gray40", hover_color="gray30").pack(side="left")

        self.table_auteur()
        self.affichage_auteur()
        self.menu_contextuelle_auteur()

    # ── Tableau ────────────────────────────────────────────────────────────
    def table_auteur(self):
        tree_frame = ctk.CTkFrame(self.parent, corner_radius=10)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        style = ttk.Style()
        style.configure("Treeview",
            background="#ffffff", foreground="#2b2b2b",
            fieldbackground="#ffffff", font=("Segoe UI", 11), rowheight=32)
        style.configure("Treeview.Heading",
            background="#1976D2", foreground="white",
            font=("Segoe UI", 12, "bold"))

        colonne = ("nom", "prenom", "date", "pays")
        self.table = ttk.Treeview(tree_frame, columns=colonne, show="headings")
        self.table.heading("nom",    text="✍️ Nom")
        self.table.heading("prenom", text="📛 Prénom")
        self.table.heading("date",   text="📅 Naissance")
        self.table.heading("pays",   text="🌍 Pays")
        self.table.column("nom",    width=200)
        self.table.column("prenom", width=200)
        self.table.column("date",   width=120)
        self.table.column("pays",   width=200)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y")

    def affichage_auteur(self):
        for item in self.table.get_children():
            self.table.delete(item)
        # display_author → (id, nom, prenom, date_naissance, nationalite)
        for a in auteur.afficher_auteur():
            self.table.insert("", "end", values=(a[1], a[2], a[3], a[4]), tags=(a[0],))

    # ── Recherche auteur ───────────────────────────────────────────────────
    def rechercher_auteur(self):
        nom    = self.cherche_nom.get().strip()
        prenom = self.cherche_prenom.get().strip()

        if not nom and not prenom:
            messagebox.showwarning("Champs vides", "Veuillez renseigner au moins le nom !")
            return

        for item in self.table.get_children():
            self.table.delete(item)

        if nom and prenom:
            # Recherche exacte nom + prénom via le contrôleur
            try:
                infos = auteur.rechercher_auteur(nom, prenom)
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))
                return
            if infos:
                # rechercher_auteur → (nom, prenom, date_naissance, nationalite)
                id_a = auteur.retourne_id_auteur(nom, prenom)
                self.table.insert("", "end", values=(infos[0], infos[1], infos[2], infos[3]), tags=(id_a,))
            else:
                messagebox.showinfo("Non trouvé", f"Aucun auteur '{nom} {prenom}' trouvé.")
        else:
            # Filtrage local sur le nom uniquement
            tous   = auteur.afficher_auteur()
            filtre = [a for a in tous if nom.lower() in a[1].lower()]
            if filtre:
                for a in filtre:
                    self.table.insert("", "end", values=(a[1], a[2], a[3], a[4]), tags=(a[0],))
            else:
                messagebox.showinfo("Non trouvé", f"Aucun auteur contenant '{nom}'.")

    # ── Ajout auteur ───────────────────────────────────────────────────────
    def ajouter_auteur(self):
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Nouvel auteur")
        popup.geometry("500x450")
        popup.grab_set()
        self.bt.configure(state="disabled")
        bind_close_reactivate(popup, self.bt)

        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(main, text="✍️ Nouvel auteur", font=("Segoe UI", 20, "bold")).pack(pady=(0, 25))

        ctk.CTkLabel(main, text="Nom *",              font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        nom_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        nom_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Prénom *",           font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        prenom_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        prenom_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Année de naissance", font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 5))
        date_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        date_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Pays",               font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 5))
        pays_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        pays_entry.pack(pady=(0, 20))

        def valider():
            nom    = nom_entry.get().strip()
            prenom = prenom_entry.get().strip()
            date   = date_entry.get().strip()
            pays   = pays_entry.get().strip()
            try:
                auteur.get_or_create_auteur(nom, prenom, date, pays)
                messagebox.showinfo("Succès", f"✓ '{nom} {prenom}' ajouté !")
                self.affichage_auteur()
                popup.destroy()
                self.bt.configure(state="normal")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(10, 0))
        ctk.CTkButton(btn_frame, text="✓ Ajouter", command=valider, width=170, height=40, corner_radius=8, fg_color="#4CAF50").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✕ Annuler",
            command=lambda: [popup.destroy(), self.bt.configure(state="normal")],
            width=170, height=40, corner_radius=8, fg_color="gray40").pack(side="left", padx=5)

    # ── Modification auteur ────────────────────────────────────────────────
    def modifier_auteur(self):
        selection = self.table.selection()
        if not selection:
            return
        id_auteur_sel = self.table.item(selection[0], "tags")[0]
        infos = auteur.recherche_auteur_par_id(int(id_auteur_sel))
        # infos → (nom, prenom, date_naissance, nationalite)
        if not infos:
            messagebox.showerror("Erreur", "Auteur introuvable !")
            return

        popup = ctk.CTkToplevel(self.parent)
        popup.title("Modifier auteur")
        popup.geometry("500x480")
        popup.grab_set()
        bind_close_reactivate(popup, None)

        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(main, text="✏️ Modifier auteur", font=("Segoe UI", 20, "bold")).pack(pady=(0, 25))

        ctk.CTkLabel(main, text="Nom *",    font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        nom_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        nom_entry.insert(0, infos[0])
        nom_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Prénom *", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        prenom_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        prenom_entry.insert(0, infos[1] or "")
        prenom_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Année de naissance *", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        date_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        date_entry.insert(0, str(infos[2]) if infos[2] else "")
        date_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Pays *",   font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        pays_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        pays_entry.insert(0, infos[3] or "")
        pays_entry.pack(pady=(0, 20))

        def valider():
            nom    = nom_entry.get().strip()
            prenom = prenom_entry.get().strip()
            date   = date_entry.get().strip()
            pays   = pays_entry.get().strip()
            try:
                auteur.modifier_auteur(nom, prenom, date, pays)
                messagebox.showinfo("Succès", f"✓ '{nom} {prenom}' modifié !")
                self.affichage_auteur()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(10, 0))
        ctk.CTkButton(btn_frame, text="💾 Sauvegarder", command=valider, width=170, height=40, corner_radius=8, fg_color="#2196F3").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✕ Annuler", command=popup.destroy, width=170, height=40, corner_radius=8, fg_color="gray40").pack(side="left", padx=5)

    # ── Menu contextuel ────────────────────────────────────────────────────
    def menu_contextuelle_auteur(self):
        import tkinter as tk
        self.menu = tk.Menu(self.parent, tearoff=0)
        self.menu.add_command(label="✏️ Modifier",  command=self.modifier_auteur)
        self.menu.add_separator()
        self.menu.add_command(label="🗑️ Supprimer", command=self.supprimer_auteur)
        self.table.bind("<Button-3>", self.afficher_menu)

    def afficher_menu(self, event):
        ligne = self.table.identify_row(event.y)
        if ligne:
            self.table.selection_set(ligne)
            self.menu.post(event.x_root, event.y_root)

    def supprimer_auteur(self):
        selection = self.table.selection()
        if not selection:
            return
        id_auteur_sel = self.table.item(selection[0], "tags")[0]
        infos = auteur.recherche_auteur_par_id(int(id_auteur_sel))
        if messagebox.askyesno("Confirmation", f"Supprimer '{infos[0]} {infos[1]}' ?\n\nIrréversible !"):
            try:
                auteur.supprimer_auteur(infos[0], infos[1])
                messagebox.showinfo("Succès", f"✓ '{infos[0]} {infos[1]}' supprimé !")
                self.affichage_auteur()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))


# =============================================================================
#  UTILISATEURS
# =============================================================================
class USER_GUI:
    def __init__(self, parent):
        self.parent = parent

        # Header avec bouton + barre de recherche
        header = ctk.CTkFrame(self.parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        self.bt = ctk.CTkButton(
            header, text="+ Nouvel utilisateur",
            command=self.ajouter_utilisateur,
            width=180, height=40, corner_radius=10,
            font=("Segoe UI", 13, "bold")
        )
        self.bt.pack(side="left", padx=(0, 20))

        self.cherche_nom    = ctk.CTkEntry(header, placeholder_text="Nom",    width=160, height=40, corner_radius=8)
        self.cherche_nom.pack(side="left", padx=(0, 8))

        self.cherche_prenom = ctk.CTkEntry(header, placeholder_text="Prénom", width=160, height=40, corner_radius=8)
        self.cherche_prenom.pack(side="left", padx=(0, 8))

        ctk.CTkButton(header, text="🔍 Rechercher", command=self.rechercher_utilisateur,
            width=130, height=40, corner_radius=8,
            fg_color="#2196F3", hover_color="#1976D2").pack(side="left", padx=(0, 8))

        ctk.CTkButton(header, text="Afficher tout", command=self.afficher_utilisateurs,
            width=120, height=40, corner_radius=8,
            fg_color="gray40", hover_color="gray30").pack(side="left")

        self.table_utilisateurs()
        self.afficher_utilisateurs()
        self.menu_contextuelle_utilisateurs()

    # ── Tableau ────────────────────────────────────────────────────────────
    def table_utilisateurs(self):
        tree_frame = ctk.CTkFrame(self.parent, corner_radius=10)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        colonne = ("nom", "prenom", "adresse")
        self.table = ttk.Treeview(tree_frame, columns=colonne, show="headings")
        self.table.heading("nom",     text="👤 Nom")
        self.table.heading("prenom",  text="📛 Prénom")
        self.table.heading("adresse", text="📍 Adresse")
        self.table.column("nom",     width=200)
        self.table.column("prenom",  width=200)
        self.table.column("adresse", width=400)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y")

    def afficher_utilisateurs(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for u in utilisateur.display_utilisateur():
            self.table.insert("", "end", values=(u[1], u[2], u[3]), tags=(u[0],))

    # ── Recherche utilisateur ──────────────────────────────────────────────
    def rechercher_utilisateur(self):
        nom    = self.cherche_nom.get().strip()
        prenom = self.cherche_prenom.get().strip()

        if not nom and not prenom:
            messagebox.showwarning("Champs vides", "Veuillez renseigner au moins le nom !")
            return

        for item in self.table.get_children():
            self.table.delete(item)

        if nom and prenom:
            # Recherche exacte nom + prénom via le contrôleur
            try:
                infos = utilisateur.rechercher_utilisateur(nom, prenom)
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))
                return
            if infos:
                # rechercher_utilisateur → (id, nom, prenom, adresse, mdp)
                self.table.insert("", "end", values=(infos[1], infos[2], infos[3]), tags=(infos[0],))
            else:
                messagebox.showinfo("Non trouvé", f"Aucun utilisateur '{nom} {prenom}' trouvé.")
        else:
            # Filtrage local sur le nom uniquement
            tous   = utilisateur.display_utilisateur()
            filtre = [u for u in tous if nom.lower() in u[1].lower()]
            if filtre:
                for u in filtre:
                    self.table.insert("", "end", values=(u[1], u[2], u[3]), tags=(u[0],))
            else:
                messagebox.showinfo("Non trouvé", f"Aucun utilisateur contenant '{nom}'.")

    # ── Ajout utilisateur ─────────────────────────────────────────────────
    def ajouter_utilisateur(self):
        popup = ctk.CTkToplevel(self.parent)
        popup.title("Nouvel utilisateur")
        popup.geometry("500x500")
        popup.grab_set()
        self.bt.configure(state="disabled")
        bind_close_reactivate(popup, self.bt)

        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(main, text="👤 Nouvel utilisateur", font=("Segoe UI", 20, "bold")).pack(pady=(0, 25))

        ctk.CTkLabel(main, text="Nom *",          font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        nom_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        nom_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Prénom *",       font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        prenom_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        prenom_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Adresse *",      font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        adresse_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        adresse_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Mot de passe *", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        mdp_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8, show="*")
        mdp_entry.pack(pady=(0, 20))

        def valider():
            nom     = nom_entry.get().strip()
            prenom  = prenom_entry.get().strip()
            adresse = adresse_entry.get().strip()
            mdp     = mdp_entry.get().strip()
            try:
                utilisateur.ajout_utilisateur(nom, prenom, adresse, mdp)
                messagebox.showinfo("Succès", f"✓ '{nom} {prenom}' ajouté !")
                self.afficher_utilisateurs()
                popup.destroy()
                self.bt.configure(state="normal")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(10, 0))
        ctk.CTkButton(btn_frame, text="✓ Ajouter", command=valider, width=170, height=40, corner_radius=8, fg_color="#4CAF50").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✕ Annuler",
            command=lambda: [popup.destroy(), self.bt.configure(state="normal")],
            width=170, height=40, corner_radius=8, fg_color="gray40").pack(side="left", padx=5)

    # ── Modification utilisateur ───────────────────────────────────────────
    def modifier_utilisateur(self):
        selection = self.table.selection()
        if not selection:
            return
        id_user = self.table.item(selection[0], "tags")[0]
        infos = utilisateur.afficher(int(id_user))
        # infos → (id, nom, prenom, adresse, mdp)
        if not infos:
            messagebox.showerror("Erreur", "Utilisateur introuvable !")
            return

        popup = ctk.CTkToplevel(self.parent)
        popup.title("Modifier utilisateur")
        popup.geometry("500x520")
        popup.grab_set()
        bind_close_reactivate(popup, None)

        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(main, text="✏️ Modifier utilisateur", font=("Segoe UI", 20, "bold")).pack(pady=(0, 25))

        ctk.CTkLabel(main, text="Nom *",    font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        nom_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        nom_entry.insert(0, infos[1])
        nom_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Prénom *", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 5))
        prenom_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        prenom_entry.insert(0, infos[2])
        prenom_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Adresse",  font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 5))
        adresse_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8)
        adresse_entry.insert(0, infos[3] or "")
        adresse_entry.pack(pady=(0, 12))

        ctk.CTkLabel(main, text="Nouveau mot de passe (vide = inchangé)", font=("Segoe UI", 11)).pack(anchor="w", pady=(0, 5))
        mdp_entry = ctk.CTkEntry(main, width=380, height=40, corner_radius=8, show="*")
        mdp_entry.pack(pady=(0, 20))

        def valider():
            nom     = nom_entry.get().strip()
            prenom  = prenom_entry.get().strip()
            adresse = adresse_entry.get().strip()
            mdp     = mdp_entry.get().strip() or None
            try:
                utilisateur.modifier_utilisateur(nom, prenom, adresse, mdp)
                messagebox.showinfo("Succès", f"✓ '{nom} {prenom}' modifié !")
                self.afficher_utilisateurs()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(10, 0))
        ctk.CTkButton(btn_frame, text="💾 Sauvegarder", command=valider, width=170, height=40, corner_radius=8, fg_color="#2196F3").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✕ Annuler", command=popup.destroy, width=170, height=40, corner_radius=8, fg_color="gray40").pack(side="left", padx=5)

    # ── Menu contextuel ────────────────────────────────────────────────────
    def menu_contextuelle_utilisateurs(self):
        import tkinter as tk
        self.menu = tk.Menu(self.parent, tearoff=0)
        self.menu.add_command(label="✏️ Modifier",  command=self.modifier_utilisateur)
        self.menu.add_separator()
        self.menu.add_command(label="🗑️ Supprimer", command=self.supprimer_utilisateurs)
        self.table.bind("<Button-3>", self.afficher_menu)

    def afficher_menu(self, event):
        ligne = self.table.identify_row(event.y)
        if ligne:
            self.table.selection_set(ligne)
            self.menu.post(event.x_root, event.y_root)

    def supprimer_utilisateurs(self):
        selection = self.table.selection()
        if not selection:
            return
        id_user = self.table.item(selection[0], "tags")[0]
        infos = utilisateur.afficher(int(id_user))
        if messagebox.askyesno("Confirmation", f"Supprimer '{infos[1]} {infos[2]}' ?"):
            try:
                utilisateur.delete_utilisateur(infos[1], infos[2])
                messagebox.showinfo("Succès", f"✓ '{infos[1]} {infos[2]}' supprimé !")
                self.afficher_utilisateurs()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))


# =============================================================================
#  EMPRUNTS
# =============================================================================
class Emprunt_GUI:
    def __init__(self, parent):
        self.parent = parent

        header = ctk.CTkFrame(self.parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(10, 0))

        ctk.CTkButton(header, text="📋 Tous les emprunts", command=self.afficher_emprunt,
            width=160, height=40, corner_radius=10).pack(side="left", padx=(0, 10))
        ctk.CTkButton(header, text="⚠️ Livres en retard", command=self.afficher_retard,
            width=160, height=40, corner_radius=10,
            fg_color="#f44336", hover_color="#d32f2f").pack(side="left")

        self.rechercher_emprunt_utilisateur()
        self.table_emprunt_en_cours()

    def table_emprunt_en_cours(self):
        tree_frame = ctk.CTkFrame(self.parent, corner_radius=10)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(15, 20))

        colonne = ("nom", "titre", "date_emprunt", "date_retour_effective", "date_retour_prevue")
        self.table = ttk.Treeview(tree_frame, columns=colonne, show="headings")
        self.table.heading("nom",                   text="👤 Utilisateur")
        self.table.heading("titre",                 text="📖 Livre")
        self.table.heading("date_emprunt",          text="📅 Emprunt")
        self.table.heading("date_retour_effective", text="✅ Retour")
        self.table.heading("date_retour_prevue",    text="⏰ Retour prévu")

        style = ttk.Style()
        style.configure("Treeview",
            background="#ffffff", foreground="#2b2b2b",
            fieldbackground="#ffffff", font=("Segoe UI", 11), rowheight=32)
        style.configure("Treeview.Heading",
            background="#1976D2", foreground="white",
            font=("Segoe UI", 12, "bold"))

        self.table.tag_configure("retard", background="#ffcccc", foreground="#c62828")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y")

        self.table.bind("<Double-1>", self.details_emprunts)

    def afficher_emprunt(self):
        for item in self.table.get_children():
            self.table.delete(item)
        # afficher_emprunts → (livre_id[0], nom_user[1], titre[2], date_emprunt[3],
        #                       date_retour_eff[4], date_retour_prev[5], user_id[6])
        for borrow in emprunt.afficher_les_emprunts():
            self.table.insert("", "end",
                values=(borrow[1], borrow[2], borrow[3], borrow[4], borrow[5]),
                tags=(str(borrow[6]), str(borrow[0])))  # (user_id, livre_id)

    def afficher_retard(self):
        for item in self.table.get_children():
            self.table.delete(item)
        # livres_en_retard → (livre_id[0], nom_user[1], titre[2],
        #                      date_emprunt[3], date_retour_prev[4], user_id[5])
        retards = emprunt.retard()
        if retards:
            for late in retards:
                # ✅ FIX : user_id EN PREMIER dans les tags (position 0), "retard" en dernier
                self.table.insert("", "end",
                    values=(late[1], late[2], late[3], "En retard !", late[4]),
                    tags=(str(late[5]), str(late[0]), "retard"))
        else:
            messagebox.showinfo("Info", "Aucun retard enregistré ! ✓")

    def rechercher_emprunt_utilisateur(self):
        search_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(search_frame, text="Recherche utilisateur:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=(0, 15))

        self.nom    = ctk.CTkEntry(search_frame, placeholder_text="Nom",    width=150, height=35, corner_radius=8)
        self.nom.pack(side="left", padx=(0, 10))

        self.prenom = ctk.CTkEntry(search_frame, placeholder_text="Prénom", width=150, height=35, corner_radius=8)
        self.prenom.pack(side="left", padx=(0, 10))

        ctk.CTkButton(search_frame, text="🔍 Rechercher", command=self.afficher_recherche,
            width=130, height=35, corner_radius=8).pack(side="left")

    def afficher_recherche(self):
        nom    = self.nom.get().strip()
        prenom = self.prenom.get().strip()

        if not all([nom, prenom]):
            messagebox.showwarning("Données manquantes", "Nom et prénom requis !")
            return
        try:
            id_user       = utilisateur.retourne_id_utilisateur(nom, prenom)
            emprunts_user = emprunt.emprunt_en_cours(id_user)

            for item in self.table.get_children():
                self.table.delete(item)

            if emprunts_user:
                for emp in emprunts_user:
                    self.table.insert("", "end", values=emp)
            else:
                messagebox.showinfo("Info", f"Aucun emprunt pour {prenom} {nom}")

            self.nom.delete(0, 'end')
            self.prenom.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def details_emprunts(self, event=None):
        selection = self.table.selection()
        if not selection:
            return

        tags = self.table.item(selection[0], "tags")

        # ✅ FIX : on parcourt les tags et on prend le premier qui est un entier valide (= user_id)
        # Le tag "retard" est une chaîne non numérique et sera ignoré automatiquement
        id_user = None
        for t in tags:
            try:
                id_user = int(t)
                break
            except (ValueError, TypeError):
                continue

        if id_user is None:
            return

        try:
            infos = utilisateur.afficher(id_user)
            quota = emprunt.cota_emprunt(id_user)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        popup = ctk.CTkToplevel(self.parent)
        popup.title("Détails utilisateur")
        popup.geometry("500x350")
        popup.grab_set()

        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(main, text=f"👤 {infos[1]} {infos[2]}", font=("Segoe UI", 20, "bold")).pack(pady=(0, 25))

        info_frame = ctk.CTkFrame(main, corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(info_frame, text=f"📍 Adresse: {infos[3]}",          font=("Segoe UI", 12)).pack(padx=20, pady=10, anchor="w")
        ctk.CTkLabel(info_frame, text=f"📚 Emprunts en cours: {quota}/2", font=("Segoe UI", 12, "bold")).pack(padx=20, pady=10, anchor="w")

        ctk.CTkButton(main, text="Fermer", command=popup.destroy,
            width=150, height=40, corner_radius=8, fg_color="gray40").pack(pady=(20, 0))


# LANCEMENT
if __name__ == "__main__":
    root = ctk.CTk()
    app = GUI(root)
    root.mainloop()