import customtkinter as ctk
from tkinter import ttk, messagebox
from controleurBiblio import (
    Book_Manager, Author_Manager, User_Manager,
    Borrow_Manager, Login, Controlleur
)

# =============================================================================
#  PALETTE — un seul endroit pour changer toute l'apparence
# =============================================================================
BLEU         = "#1a73e8"
BLEU_HOVER   = "#1557b0"
BLEU_CLAIR   = "#e8f0fe"
ROUGE        = "#e53935"
ROUGE_HOVER  = "#b71c1c"
VERT         = "#2e7d32"
ORANGE       = "#e65100"
RAYON        = 14
POLICE       = "Segoe UI"

# Navigation : (clé du frame, label affiché, icône)
NAV_ADMIN = [
    ("livres",       "Livres",       "📖"),
    ("auteurs",      "Auteurs",      "✍️"),
    ("utilisateurs", "Utilisateurs", "👤"),
    ("emprunts",     "Emprunts",     "📋"),
]
NAV_USER = [
    ("catalogue",    "Catalogue",    "📖"),
    ("en_cours",     "Mes emprunts", "📋"),
    ("historique",   "Historique",   "🕘"),
]

# =============================================================================
#  INSTANCES GLOBALES
# =============================================================================
livres      = Book_Manager("test01.db")
auteur      = Author_Manager("test01.db")
utilisateur = User_Manager("test01.db")
emprunt     = Borrow_Manager("test01.db")
login       = Login("test01.db")
session     = Controlleur


# =============================================================================
#  HELPER
# =============================================================================
def bind_close_reactivate(window, button):
    def _on_close():
        window.destroy()
        if button and button.winfo_exists():
            button.configure(state="normal")
    window.protocol("WM_DELETE_WINDOW", _on_close)


# =============================================================================
#  GUI PRINCIPALE — sidebar + zone contenu
# =============================================================================
class GUI:

    def __init__(self, root, role=None):
        self.root = root
        self.role = role
        self.root.title("📚 Biblio — Gestion de Bibliothèque")
        self.root.geometry("1300x800")

        self.boutons_nav = {}      # référence aux boutons sidebar pour le surlignage
        self.vue_active  = None    # nom de la vue actuellement visible

        self._creer_layout()
        self._creer_sidebar()
        self._creer_contenu()

        # Vue affichée par défaut selon le rôle
        premiere_vue = NAV_ADMIN[0][0] if role == "admin" else NAV_USER[0][0]
        self._naviguer(premiere_vue)

    # ── Structure principale ───────────────────────────────────────────────
    def _creer_layout(self):
        """Crée les deux zones : sidebar à gauche, contenu à droite."""
        self.frame_sidebar  = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.frame_sidebar.pack(side="left", fill="y")
        self.frame_sidebar.pack_propagate(False)  # empêche le frame de rétrécir

        self.frame_contenu = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.frame_contenu.pack(side="left", fill="both", expand=True)

    # ── Sidebar ────────────────────────────────────────────────────────────
    def _creer_sidebar(self):
        # Logo
        ctk.CTkLabel(
            self.frame_sidebar,
            text="📚 Biblio",
            font=(POLICE, 20, "bold"),
            text_color=BLEU
        ).pack(pady=(30, 40), padx=20)

        # Boutons de navigation
        nav_items = NAV_ADMIN if self.role == "admin" else NAV_USER
        for cle, label, icone in nav_items:
            btn = ctk.CTkButton(
                self.frame_sidebar,
                text=f"  {icone}  {label}",
                anchor="w",
                fg_color="transparent",
                text_color=("gray20", "gray80"),
                hover_color=(BLEU_CLAIR, "#2a3a5c"),
                height=42,
                corner_radius=RAYON,
                font=(POLICE, 13),
                # ↓ lambda avec capture de valeur — le n=cle évite le piège de boucle
                command=lambda n=cle: self._naviguer(n)
            )
            btn.pack(fill="x", padx=12, pady=3)
            self.boutons_nav[cle] = btn  # on garde la référence pour le surlignage

        # Spacer — pousse les boutons du bas vers le bas
        ctk.CTkFrame(self.frame_sidebar, fg_color="transparent").pack(fill="y", expand=True)

        # Séparateur
        ctk.CTkFrame(self.frame_sidebar, height=1, fg_color=("gray80", "gray30")).pack(
            fill="x", padx=12, pady=(0, 10)
        )

        # Toggle dark / light
        ctk.CTkButton(
            self.frame_sidebar,
            text="  🌙  Dark / Light",
            anchor="w",
            fg_color="transparent",
            text_color=("gray20", "gray80"),
            hover_color=(BLEU_CLAIR, "#2a3a5c"),
            height=38,
            corner_radius=RAYON,
            font=(POLICE, 12),
            command=self._toggle_theme
        ).pack(fill="x", padx=12, pady=3)

        # Déconnexion
        ctk.CTkButton(
            self.frame_sidebar,
            text="  ←  Déconnexion",
            anchor="w",
            fg_color="transparent",
            text_color=(ROUGE, "#ff6b6b"),
            hover_color=("#fdecea", "#3a1a1a"),
            height=38,
            corner_radius=RAYON,
            font=(POLICE, 12),
            command=self._deconnexion
        ).pack(fill="x", padx=12, pady=(3, 20))

    # ── Zone contenu ───────────────────────────────────────────────────────
    def _creer_contenu(self):
        """
        Crée TOUS les frames de contenu une seule fois.
        Ils sont tous invisibles au départ — _naviguer en révèle un à la fois.
        """
        if self.role == "admin":
            self.frames = {
                "livres":       LivreAdmin_GUI(self.frame_contenu),
                "auteurs":      AuteurAdmin_GUI(self.frame_contenu),
                "utilisateurs": USER_GUI(self.frame_contenu),
                "emprunts":     Emprunt_GUI(self.frame_contenu),
            }
        else:
            self.frames = {
                "catalogue":  LivresCatalogue_GUI(self.frame_contenu),
                "en_cours":   Emprunt_en_cours(self.frame_contenu),
                "historique": Borrow_History(self.frame_contenu),
            }

    # ── Navigation ─────────────────────────────────────────────────────────
    def _naviguer(self, nom_vue):
        """
        Cache tous les frames, révèle uniquement celui demandé,
        et met à jour le surlignage du bouton actif dans la sidebar.
        """
        # 1. Cacher tous les frames
        for frame in self.frames.values():
            frame.pack_forget()

        # 2. Révéler uniquement la vue demandée
        self.frames[nom_vue].pack(fill="both", expand=True, padx=20, pady=20)

        # 3. Mettre à jour l'apparence des boutons sidebar
        for cle, btn in self.boutons_nav.items():
            if cle == nom_vue:
                # Bouton actif : fond coloré
                btn.configure(fg_color=(BLEU_CLAIR, "#1e3a6e"), text_color=(BLEU, "#7ab3ff"))
            else:
                # Boutons inactifs : transparent
                btn.configure(fg_color="transparent", text_color=("gray20", "gray80"))

        self.vue_active = nom_vue

    # ── Toggle thème ───────────────────────────────────────────────────────
    def _toggle_theme(self):
        mode_actuel = ctk.get_appearance_mode()   # retourne "Dark" ou "Light"
        nouveau     = "light" if mode_actuel == "Dark" else "dark"
        ctk.set_appearance_mode(nouveau)

    # ── Déconnexion ────────────────────────────────────────────────────────
    def _deconnexion(self):
        # Sécurité : vider la session avant tout
        Controlleur.current_user = None
        # Détruire tous les widgets de la fenêtre
        for widget in self.root.winfo_children():
            widget.destroy()
        # Recréer la page de connexion
        app = Login_GUI(self.root)
        app.connexion()


# =============================================================================
#  HELPER UI — cards et tableaux réutilisables
# =============================================================================

def creer_tableau(parent, colonnes: dict, tag_retard=False):
    """
    Crée un tableau (ttk.Treeview) stylisé et le retourne.
    colonnes = {"clé": ("Titre affiché", largeur), ...}
    """
    frame = ctk.CTkFrame(parent, corner_radius=RAYON)
    frame.pack(fill="both", expand=True, pady=(10, 0))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Biblio.Treeview",
        background="#ffffff", foreground="#1a1a2e",
        fieldbackground="#ffffff", borderwidth=0,
        font=(POLICE, 11), rowheight=36)
    style.configure("Biblio.Treeview.Heading",
        background=BLEU, foreground="white",
        font=(POLICE, 11, "bold"), borderwidth=0, relief="flat")
    style.map("Biblio.Treeview",
        background=[("selected", BLEU)],
        foreground=[("selected", "white")])

    table = ttk.Treeview(
        frame,
        columns=list(colonnes.keys()),
        show="headings",
        style="Biblio.Treeview"
    )
    for cle, (titre, largeur) in colonnes.items():
        table.heading(cle, text=titre)
        table.column(cle, width=largeur)

    if tag_retard:
        table.tag_configure("retard", background="#ffebee", foreground="#c62828")

    scroll = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scroll.set)
    table.pack(side="left", fill="both", expand=True, padx=2, pady=2)
    scroll.pack(side="right", fill="y")

    return table


def creer_entete(parent, titre, texte_btn=None, cmd_btn=None):
    """
    Crée l'en-tête d'une section : titre à gauche, bouton optionnel à droite.
    Retourne le frame entête (pour y ajouter d'autres éléments si besoin).
    """
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", pady=(0, 10))

    ctk.CTkLabel(
        frame, text=titre,
        font=(POLICE, 20, "bold")
    ).pack(side="left")

    if texte_btn and cmd_btn:
        btn = ctk.CTkButton(
            frame, text=texte_btn, command=cmd_btn,
            width=160, height=38, corner_radius=RAYON,
            font=(POLICE, 12, "bold"),
            fg_color=BLEU, hover_color=BLEU_HOVER
        )
        btn.pack(side="right")
        return frame, btn

    return frame, None


def creer_barre_recherche(parent, placeholder, cmd_recherche, cmd_reset):
    """Barre de recherche standardisée avec bouton reset."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", pady=(0, 10))

    entry = ctk.CTkEntry(
        frame, placeholder_text=f"🔍  {placeholder}",
        height=38, corner_radius=RAYON,
        font=(POLICE, 12)
    )
    entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    ctk.CTkButton(
        frame, text="Rechercher", command=cmd_recherche,
        width=120, height=38, corner_radius=RAYON,
        fg_color=BLEU, hover_color=BLEU_HOVER,
        font=(POLICE, 12)
    ).pack(side="left", padx=(0, 6))

    ctk.CTkButton(
        frame, text="Tout afficher", command=cmd_reset,
        width=120, height=38, corner_radius=RAYON,
        fg_color=("gray80", "gray30"), hover_color=("gray70", "gray40"),
        font=(POLICE, 12)
    ).pack(side="left")

    return entry


# =============================================================================
#  LIVRES — vue admin
# =============================================================================
class LivreAdmin_GUI(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.ajout = None

        header_frame, self.btn_ajouter = creer_entete(
            self, "📖  Livres", "+ Nouveau livre", self.formulaire_ajout_livre
        )
        self.cherche = creer_barre_recherche(
            self, "Rechercher un livre...", self.afficher_recherche, self.afficher_livre
        )
        self.tableau = creer_tableau(self, {
            "auteur": ("✍️ Auteur",  240),
            "titre":  ("📖 Titre",   320),
            "genre":  ("🎭 Genre",   160),
            "etat":   ("📊 État",    120),
            "stock":  ("📦 Stock",    80),
        })
        self.tableau.bind("<Double-1>", self.afficher_details)
        self._creer_menu_contextuel()
        self.afficher_livre()

    def afficher_livre(self):
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        for l in livres.afficher_livre():
            self.tableau.insert("", "end",
                values=(f"{l[1]} {l[2]}", l[3], l[5], l[6], l[7]),
                tags=(l[0],))

    def afficher_recherche(self):
        terme = self.cherche.get().strip()
        if not terme:
            messagebox.showwarning("Champ vide", "Veuillez saisir un titre !")
            return
        livre = livres.rechercher(terme)
        if not livre:
            messagebox.showinfo("Non trouvé", f"'{terme}' introuvable.")
            self.cherche.delete(0, ctk.END)
            return
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        id_book = livres.book_id(terme)
        self.tableau.insert("", "end",
            values=(f"{livre[0]} {livre[1]}", livre[2], livre[4], livre[5], livre[6]),
            tags=(id_book,))
        self.cherche.delete(0, ctk.END)

    def _creer_menu_contextuel(self):
        import tkinter as tk
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="👁️ Détails",  command=lambda: self.afficher_details(mode=False))
        self.menu.add_separator()
        self.menu.add_command(label="✏️ Modifier",  command=lambda: self.afficher_details(mode=True))
        self.menu.add_separator()
        self.menu.add_command(label="🗑️ Supprimer", command=self.supprimer_livre)
        self.tableau.bind("<Button-3>", lambda e: self._afficher_menu(e))

    def _afficher_menu(self, event):
        ligne = self.tableau.identify_row(event.y)
        if ligne:
            self.tableau.selection_set(ligne)
            self.menu.post(event.x_root, event.y_root)

    def supprimer_livre(self):
        selection = self.tableau.selection()
        if not selection:
            return
        id_livre = self.tableau.item(selection[0], "tags")[0]
        info = livres.recherche_par_id(int(id_livre))
        if messagebox.askyesno("Confirmation", f"Supprimer '{info[2]}' ?\nCette action est irréversible !"):
            try:
                livres.supprimer_livre(info[2])
                messagebox.showinfo("Succès", f"✓ '{info[2]}' supprimé !")
                self.afficher_livre()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def selection(self, livre_id=None):
        sel = self.tableau.selection()
        if not sel:
            return None
        return self.tableau.item(sel[0], "tags")[0]

    def afficher_details(self, event=None, livre_id=None, mode=None):
        if event or livre_id is None:
            livre_id = self.selection()
        if livre_id is None:
            return
        self._id = int(livre_id)
        info = livres.recherche_par_id(self._id)

        import tkinter as tk
        self._details = tk.Toplevel(self)
        self._details.title(f"Détails : {info[2]}")
        self._details.geometry("640x300")
        self._details.grab_set()

        self._dict_orig = {"titre": info[2], "date": info[3], "genre": info[4], "etat": info[5], "stock": info[6]}

        for i, (label, val, attr) in enumerate([
            ("Titre",  info[2], "titre"),
            ("Auteur", f"{info[0]} {info[1]}", None),
            ("Date",   info[3], "date"),
            ("Genre",  info[4], "genre"),
            ("État",   info[5], "etat"),
            ("Stock",  info[6], "stock"),
        ]):
            row, col = divmod(i, 2)
            tk.Label(self._details, text=f"{label}:", font=(POLICE, 10, "bold")).grid(
                row=row*2, column=col*2, padx=12, pady=(12, 2), sticky="w")
            var = tk.StringVar(value=str(val) if val else "")
            entry = tk.Entry(self._details, textvariable=var,
                state="readonly", font=(POLICE, 10), width=22)
            entry.grid(row=row*2+1, column=col*2, padx=12, pady=(0, 8))
            if attr:
                setattr(self, f"_var_{attr}", var)
                setattr(self, f"_entry_{attr}", entry)

        if mode:
            import tkinter as tk
            tk.Button(self._details, text="✏️ Modifier", command=self._activar_edicion,
                bg=BLEU, fg="white", font=(POLICE, 10, "bold"), width=12).grid(
                row=6, column=1, pady=15)

    def _activar_edicion(self):
        import tkinter as tk
        for attr in ["titre", "date", "genre", "etat", "stock"]:
            getattr(self, f"_entry_{attr}").config(state="normal")
        tk.Button(self._details, text="💾 Sauvegarder",
            command=self._sauvegardar,
            bg=VERT, fg="white", font=(POLICE, 10, "bold"), width=12).grid(row=6, column=1, pady=15)

    def _sauvegardar(self):
        stock = self._var_stock.get()
        date  = self._var_date.get()
        if not (stock.isdigit() and date.isdigit()):
            messagebox.showwarning("Attention", "La quantité et la date doivent être des nombres !")
            return
        nouveau = {
            "titre": self._var_titre.get(),
            "date":  int(date),
            "genre": self._var_genre.get(),
            "etat":  self._var_etat.get(),
            "stock": int(stock)
        }
        if self._dict_orig == nouveau:
            messagebox.showinfo("Aucun changement", "Aucune modification détectée.")
            return
        if messagebox.askyesno("Confirmation", "Enregistrer les modifications ?"):
            livres.modifier_livre(self._id, nouveau["titre"], nouveau["date"],
                                  nouveau["genre"], nouveau["etat"], nouveau["stock"])
            messagebox.showinfo("Succès", f"✓ '{nouveau['titre']}' modifié !")
            self._details.destroy()
            self.afficher_livre()

    def formulaire_ajout_livre(self):
        self.ajout = ctk.CTkToplevel(self)
        self.ajout.title("Nouveau livre")
        self.ajout.geometry("680x640")
        self.ajout.resizable(False, False)
        self.ajout.grab_set()
        self.btn_ajouter.configure(state="disabled")
        bind_close_reactivate(self.ajout, self.btn_ajouter)

        main = ctk.CTkFrame(self.ajout, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(main, text="📖  Ajouter un nouveau livre",
            font=(POLICE, 20, "bold")).pack(pady=(0, 24))

        ff = ctk.CTkFrame(main, fg_color="transparent")
        ff.pack(fill="both", expand=True)

        champs = [
            ("Titre *",          "titre_livre",        0, 0),
            ("Nom auteur *",     "auteur_nom_livre",   0, 1),
            ("Prénom auteur *",  "auteur_prenom_livre",1, 0),
            ("Année",            "date_livre",         1, 1),
            ("Genre",            "genre_livre",        2, 0),
            ("Quantité",         "qte",                2, 1),
            ("État *",           "state",              3, 0),
        ]
        for label, attr, row, col in champs:
            is_required = "*" in label
            ctk.CTkLabel(ff, text=label,
                font=(POLICE, 12, "bold" if is_required else "normal"),
                text_color=(ROUGE if is_required else ("gray40", "gray60"))
            ).grid(row=row*2, column=col, sticky="w", pady=(0, 4), padx=(0 if col else 0, 15))
            entry = ctk.CTkEntry(ff, width=270, height=38, corner_radius=RAYON)
            entry.grid(row=row*2+1, column=col, pady=(0, 16), padx=(0, 15))
            setattr(self, attr, entry)

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(8, 0))

        ctk.CTkButton(btn_frame, text="✓ Ajouter", command=self.validation_ajout_livre,
            width=180, height=42, corner_radius=RAYON,
            font=(POLICE, 13, "bold"), fg_color=VERT, hover_color="#1b5e20"
        ).pack(side="left", padx=8)

        ctk.CTkButton(btn_frame, text="✕ Annuler", command=self.fermer_formulaire,
            width=180, height=42, corner_radius=RAYON,
            font=(POLICE, 13, "bold"), fg_color=("gray70", "gray40"), hover_color=("gray60", "gray30")
        ).pack(side="left", padx=8)

    def validation_ajout_livre(self):
        nom        = self.auteur_nom_livre.get().strip()
        prenom     = self.auteur_prenom_livre.get().strip()
        titre_book = self.titre_livre.get().strip()
        date       = self.date_livre.get().strip()
        etat_book  = self.state.get().strip()
        qtes       = self.qte.get().strip()
        cat        = self.genre_livre.get().strip()

        if not all([nom, prenom, titre_book, etat_book]):
            messagebox.showwarning("Champs manquants", "Titre, auteur et état sont requis !")
            return
        if auteur.retourne_id_auteur(nom, prenom) is None:
            if messagebox.askyesno("Auteur inconnu", f"{nom} {prenom} n'est pas enregistré. L'ajouter ?"):
                if self._popup_auteur(nom, prenom) is None:
                    return
            else:
                return
        try:
            resultat = livres.ajouter_livre(
                titre_book, nom, prenom, None, None,
                etat_book, date or None, qtes or None, cat or None
            )
            if resultat:
                messagebox.showinfo("Succès", f"✓ '{titre_book}' ajouté !")
                self.afficher_livre()
                self.fermer_formulaire()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _popup_auteur(self, nom, prenom):
        win = ctk.CTkToplevel(self.ajout)
        win.title("Informations auteur")
        win.geometry("440x280")
        win.grab_set()

        main = ctk.CTkFrame(win, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(main, text=f"Auteur : {nom} {prenom}",
            font=(POLICE, 14, "bold")).pack(pady=(0, 20))

        ctk.CTkLabel(main, text="Année de naissance", font=(POLICE, 12)).pack(anchor="w")
        date_entry = ctk.CTkEntry(main, width=340, height=36, corner_radius=RAYON)
        date_entry.pack(pady=(4, 12))

        ctk.CTkLabel(main, text="Pays", font=(POLICE, 12)).pack(anchor="w")
        pays_entry = ctk.CTkEntry(main, width=340, height=36, corner_radius=RAYON)
        pays_entry.pack(pady=(4, 20))

        resultat = [None]

        def valider():
            try:
                auteur.get_or_create_auteur(nom, prenom,
                    date_entry.get().strip(), pays_entry.get().strip())
                resultat[0] = True
                win.destroy()
            except Exception as e:
                messagebox.showwarning("Attention", str(e), parent=win)

        ctk.CTkButton(main, text="Ajouter", command=valider,
            width=150, height=36, corner_radius=RAYON, fg_color=BLEU).pack(side="left", padx=5)
        ctk.CTkButton(main, text="Annuler", command=win.destroy,
            width=150, height=36, corner_radius=RAYON,
            fg_color=("gray70", "gray40")).pack(side="left", padx=5)

        win.wait_window()
        return resultat[0]

    def fermer_formulaire(self):
        if self.ajout and self.ajout.winfo_exists():
            self.ajout.destroy()
            self.ajout = None
        if self.btn_ajouter.winfo_exists():
            self.btn_ajouter.configure(state="normal")


# =============================================================================
#  LIVRES — vue utilisateur (catalogue)
# =============================================================================
class LivresCatalogue_GUI(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        creer_entete(self, "📖  Catalogue")
        self.cherche = creer_barre_recherche(
            self, "Rechercher un livre...", self.afficher_recherche, self.afficher_livre
        )
        self.tableau = creer_tableau(self, {
            "auteur": ("✍️ Auteur",  260),
            "titre":  ("📖 Titre",   340),
            "genre":  ("🎭 Genre",   180),
            "etat":   ("📊 État",    140),
        })
        self.afficher_livre()

    def afficher_livre(self):
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        for l in livres.afficher_livre():
            self.tableau.insert("", "end",
                values=(f"{l[1]} {l[2]}", l[3], l[5], l[6]),
                tags=(l[0],))

    def afficher_recherche(self):
        terme = self.cherche.get().strip()
        if not terme:
            messagebox.showwarning("Champ vide", "Veuillez saisir un titre !")
            return
        livre = livres.rechercher(terme)
        if not livre:
            messagebox.showinfo("Non trouvé", f"'{terme}' introuvable.")
            self.cherche.delete(0, ctk.END)
            return
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        id_book = livres.book_id(terme)
        self.tableau.insert("", "end",
            values=(f"{livre[0]} {livre[1]}", livre[2], livre[4], livre[5]),
            tags=(id_book,))
        self.cherche.delete(0, ctk.END)


# =============================================================================
#  AUTEURS
# =============================================================================
class AuteurAdmin_GUI(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        header_frame, self.bt = creer_entete(
            self, "✍️  Auteurs", "+ Nouvel auteur", self.ajouter_auteur
        )

        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.pack(side="right", padx=(0, 16))
        self.cherche_nom    = ctk.CTkEntry(search_frame, placeholder_text="Nom",    width=140, height=36, corner_radius=RAYON)
        self.cherche_prenom = ctk.CTkEntry(search_frame, placeholder_text="Prénom", width=140, height=36, corner_radius=RAYON)
        self.cherche_nom.pack(side="left", padx=(0, 6))
        self.cherche_prenom.pack(side="left", padx=(0, 6))
        ctk.CTkButton(search_frame, text="🔍", command=self.rechercher_auteur,
            width=38, height=36, corner_radius=RAYON, fg_color=BLEU).pack(side="left", padx=(0, 6))
        ctk.CTkButton(search_frame, text="✕", command=self.affichage_auteur,
            width=38, height=36, corner_radius=RAYON,
            fg_color=("gray70", "gray40")).pack(side="left")

        self.table = creer_tableau(self, {
            "nom":    ("✍️ Nom",        200),
            "prenom": ("📛 Prénom",      200),
            "date":   ("📅 Naissance",   120),
            "pays":   ("🌍 Nationalité", 200),
        })
        self._creer_menu_contextuel()
        self.affichage_auteur()

    def affichage_auteur(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for a in auteur.afficher_auteur():
            self.table.insert("", "end", values=(a[1], a[2], a[3], a[4]), tags=(a[0],))

    def rechercher_auteur(self):
        nom    = self.cherche_nom.get().strip()
        prenom = self.cherche_prenom.get().strip()
        if not nom and not prenom:
            messagebox.showwarning("Champs vides", "Renseignez au moins le nom !")
            return
        for item in self.table.get_children():
            self.table.delete(item)
        if nom and prenom:
            try:
                infos = auteur.rechercher_auteur(nom, prenom)
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))
                return
            if infos:
                id_a = auteur.retourne_id_auteur(nom, prenom)
                self.table.insert("", "end", values=(infos[0], infos[1], infos[2], infos[3]), tags=(id_a,))
            else:
                messagebox.showinfo("Non trouvé", f"Aucun auteur '{nom} {prenom}'.")
        else:
            tous   = auteur.afficher_auteur()
            filtre = [a for a in tous if nom.lower() in a[1].lower()]
            for a in filtre:
                self.table.insert("", "end", values=(a[1], a[2], a[3], a[4]), tags=(a[0],))
            if not filtre:
                messagebox.showinfo("Non trouvé", f"Aucun auteur contenant '{nom}'.")
        self.cherche_nom.delete(0, ctk.END)
        self.cherche_prenom.delete(0, ctk.END)

    def ajouter_auteur(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Nouvel auteur")
        popup.geometry("480x440")
        popup.grab_set()
        self.bt.configure(state="disabled")
        bind_close_reactivate(popup, self.bt)

        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(main, text="✍️  Nouvel auteur",
            font=(POLICE, 20, "bold")).pack(pady=(0, 24))

        champs = [("Nom *", True), ("Prénom *", True),
                  ("Année de naissance", False), ("Pays", False)]
        entries = []
        for label, required in champs:
            ctk.CTkLabel(main, text=label,
                font=(POLICE, 12, "bold" if required else "normal"),
                text_color=(ROUGE if required else ("gray40", "gray60"))
            ).pack(anchor="w", pady=(0, 4))
            e = ctk.CTkEntry(main, width=380, height=38, corner_radius=RAYON)
            e.pack(pady=(0, 12))
            entries.append(e)

        def valider():
            try:
                auteur.get_or_create_auteur(
                    entries[0].get().strip(), entries[1].get().strip(),
                    entries[2].get().strip(), entries[3].get().strip()
                )
                messagebox.showinfo("Succès", f"✓ '{entries[0].get()} {entries[1].get()}' ajouté !")
                self.affichage_auteur()
                popup.destroy()
                self.bt.configure(state="normal")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(8, 0))
        ctk.CTkButton(btn_frame, text="✓ Ajouter", command=valider,
            width=170, height=40, corner_radius=RAYON, fg_color=VERT).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✕ Annuler",
            command=lambda: [popup.destroy(), self.bt.configure(state="normal")],
            width=170, height=40, corner_radius=RAYON,
            fg_color=("gray70", "gray40")).pack(side="left", padx=5)

    def modifier_auteur(self):
        selection = self.table.selection()
        if not selection:
            return
        id_sel = self.table.item(selection[0], "tags")[0]
        infos  = auteur.recherche_auteur_par_id(int(id_sel))
        if not infos:
            messagebox.showerror("Erreur", "Auteur introuvable !")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Modifier auteur")
        popup.geometry("480x440")
        popup.grab_set()

        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(main, text="✏️  Modifier auteur",
            font=(POLICE, 20, "bold")).pack(pady=(0, 24))

        valeurs  = [infos[0], infos[1] or "", str(infos[2]) if infos[2] else "", infos[3] or ""]
        labels   = ["Nom *", "Prénom *", "Année de naissance", "Pays"]
        entries  = []
        for label, val in zip(labels, valeurs):
            required = "*" in label
            ctk.CTkLabel(main, text=label,
                font=(POLICE, 12, "bold" if required else "normal"),
                text_color=(ROUGE if required else ("gray40", "gray60"))
            ).pack(anchor="w", pady=(0, 4))
            e = ctk.CTkEntry(main, width=380, height=38, corner_radius=RAYON)
            e.insert(0, val)
            e.pack(pady=(0, 12))
            entries.append(e)

        def valider():
            try:
                auteur.modifier_auteur(
                    entries[0].get().strip(), entries[1].get().strip(),
                    entries[2].get().strip() or None,
                    entries[3].get().strip() or None
                )
                messagebox.showinfo("Succès", f"✓ Auteur modifié !")
                self.affichage_auteur()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(8, 0))
        ctk.CTkButton(btn_frame, text="💾 Sauvegarder", command=valider,
            width=170, height=40, corner_radius=RAYON, fg_color=BLEU).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✕ Annuler", command=popup.destroy,
            width=170, height=40, corner_radius=RAYON,
            fg_color=("gray70", "gray40")).pack(side="left", padx=5)

    def supprimer_auteur(self):
        selection = self.table.selection()
        if not selection:
            return
        id_sel = self.table.item(selection[0], "tags")[0]
        infos  = auteur.recherche_auteur_par_id(int(id_sel))
        if messagebox.askyesno("Confirmation", f"Supprimer '{infos[0]} {infos[1]}' ?\nIrréversible !"):
            try:
                auteur.supprimer_auteur(infos[0], infos[1])
                messagebox.showinfo("Succès", f"✓ '{infos[0]} {infos[1]}' supprimé !")
                self.affichage_auteur()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def _creer_menu_contextuel(self):
        import tkinter as tk
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="✏️ Modifier",  command=self.modifier_auteur)
        self.menu.add_separator()
        self.menu.add_command(label="🗑️ Supprimer", command=self.supprimer_auteur)
        self.table.bind("<Button-3>", lambda e: self._afficher_menu(e))

    def _afficher_menu(self, event):
        ligne = self.table.identify_row(event.y)
        if ligne:
            self.table.selection_set(ligne)
            self.menu.post(event.x_root, event.y_root)


# =============================================================================
#  UTILISATEURS
# =============================================================================
class USER_GUI(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        header_frame, self.bt = creer_entete(
            self, "👤  Utilisateurs", "+ Nouvel utilisateur", self.ajouter_utilisateur
        )
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.pack(side="right", padx=(0, 16))
        self.cherche_nom    = ctk.CTkEntry(search_frame, placeholder_text="Nom",    width=140, height=36, corner_radius=RAYON)
        self.cherche_prenom = ctk.CTkEntry(search_frame, placeholder_text="Prénom", width=140, height=36, corner_radius=RAYON)
        self.cherche_nom.pack(side="left", padx=(0, 6))
        self.cherche_prenom.pack(side="left", padx=(0, 6))
        ctk.CTkButton(search_frame, text="🔍", command=self.rechercher_utilisateur,
            width=38, height=36, corner_radius=RAYON, fg_color=BLEU).pack(side="left", padx=(0, 6))
        ctk.CTkButton(search_frame, text="✕", command=self.afficher_utilisateurs,
            width=38, height=36, corner_radius=RAYON,
            fg_color=("gray70", "gray40")).pack(side="left")

        self.table = creer_tableau(self, {
            "nom":     ("👤 Nom",      200),
            "prenom":  ("📛 Prénom",   200),
            "adresse": ("📍 Adresse",  380),
            "role":    ("🔑 Rôle",     100),
        })
        self._creer_menu_contextuel()
        self.afficher_utilisateurs()

    def afficher_utilisateurs(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for u in utilisateur.display_utilisateur():
            self.table.insert("", "end", values=(u[1], u[2], u[3], u[5]), tags=(u[0],))

    def rechercher_utilisateur(self):
        nom    = self.cherche_nom.get().strip()
        prenom = self.cherche_prenom.get().strip()
        if not nom and not prenom:
            messagebox.showwarning("Champs vides", "Renseignez au moins le nom !")
            return
        for item in self.table.get_children():
            self.table.delete(item)
        if nom and prenom:
            try:
                infos = utilisateur.rechercher_utilisateur(nom, prenom)
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))
                return
            if infos:
                self.table.insert("", "end",
                    values=(infos[1], infos[2], infos[3], infos[5]), tags=(infos[0],))
            else:
                messagebox.showinfo("Non trouvé", f"Aucun utilisateur '{nom} {prenom}'.")
        else:
            tous   = utilisateur.display_utilisateur()
            filtre = [u for u in tous if nom.lower() in u[1].lower()]
            for u in filtre:
                self.table.insert("", "end", values=(u[1], u[2], u[3], u[5]), tags=(u[0],))
            if not filtre:
                messagebox.showinfo("Non trouvé", f"Aucun utilisateur contenant '{nom}'.")
        self.cherche_nom.delete(0, ctk.END)
        self.cherche_prenom.delete(0, ctk.END)

    def ajouter_utilisateur(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Nouvel utilisateur")
        popup.geometry("480x500")
        popup.grab_set()
        self.bt.configure(state="disabled")
        bind_close_reactivate(popup, self.bt)

        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(main, text="👤  Nouvel utilisateur",
            font=(POLICE, 20, "bold")).pack(pady=(0, 24))

        champs = [("Nom *", True), ("Prénom *", True),
                  ("Adresse *", True), ("Mot de passe *", True)]
        entries = []
        for label, required in champs:
            ctk.CTkLabel(main, text=label, font=(POLICE, 12, "bold"),
                text_color=ROUGE).pack(anchor="w", pady=(0, 4))
            e = ctk.CTkEntry(main, width=380, height=38, corner_radius=RAYON,
                show="*" if "passe" in label else "")
            e.pack(pady=(0, 12))
            entries.append(e)

        def valider():
            nom, prenom, adresse, mdp = [e.get().strip() for e in entries]
            try:
                utilisateur.ajout_utilisateur(nom, prenom, adresse, mdp, status="user")
                messagebox.showinfo("Succès", f"✓ '{nom} {prenom}' ajouté !")
                self.afficher_utilisateurs()
                popup.destroy()
                self.bt.configure(state="normal")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(8, 0))
        ctk.CTkButton(btn_frame, text="✓ Ajouter", command=valider,
            width=170, height=40, corner_radius=RAYON, fg_color=VERT).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✕ Annuler",
            command=lambda: [popup.destroy(), self.bt.configure(state="normal")],
            width=170, height=40, corner_radius=RAYON,
            fg_color=("gray70", "gray40")).pack(side="left", padx=5)

    def modifier_utilisateur(self):
        selection = self.table.selection()
        if not selection:
            return
        id_user = self.table.item(selection[0], "tags")[0]
        infos   = utilisateur.afficher(int(id_user))
        if not infos:
            messagebox.showerror("Erreur", "Utilisateur introuvable !")
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Modifier utilisateur")
        popup.geometry("480x480")
        popup.grab_set()

        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=40, pady=30)

        ctk.CTkLabel(main, text="✏️  Modifier utilisateur",
            font=(POLICE, 20, "bold")).pack(pady=(0, 24))

        labels_vals = [
            ("Nom *",    infos[1], False),
            ("Prénom *", infos[2], False),
            ("Adresse",  infos[3] or "", False),
            ("Nouveau mot de passe (vide = inchangé)", "", True),
        ]
        entries = []
        for label, val, is_pwd in labels_vals:
            ctk.CTkLabel(main, text=label, font=(POLICE, 12)).pack(anchor="w", pady=(0, 4))
            e = ctk.CTkEntry(main, width=380, height=38, corner_radius=RAYON,
                show="*" if is_pwd else "")
            e.insert(0, val)
            e.pack(pady=(0, 12))
            entries.append(e)

        def valider():
            nom, prenom, adresse, mdp = [e.get().strip() for e in entries]
            try:
                utilisateur.modifier_utilisateur(nom, prenom, adresse, mdp or None)
                messagebox.showinfo("Succès", f"✓ '{nom} {prenom}' modifié !")
                self.afficher_utilisateurs()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(pady=(8, 0))
        ctk.CTkButton(btn_frame, text="💾 Sauvegarder", command=valider,
            width=170, height=40, corner_radius=RAYON, fg_color=BLEU).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✕ Annuler", command=popup.destroy,
            width=170, height=40, corner_radius=RAYON,
            fg_color=("gray70", "gray40")).pack(side="left", padx=5)

    def supprimer_utilisateurs(self):
        selection = self.table.selection()
        if not selection:
            return
        id_user = self.table.item(selection[0], "tags")[0]
        infos   = utilisateur.afficher(int(id_user))
        if messagebox.askyesno("Confirmation", f"Supprimer '{infos[1]} {infos[2]}' ?"):
            try:
                utilisateur.delete_utilisateur(infos[1], infos[2])
                messagebox.showinfo("Succès", f"✓ '{infos[1]} {infos[2]}' supprimé !")
                self.afficher_utilisateurs()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def _creer_menu_contextuel(self):
        import tkinter as tk
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="✏️ Modifier",  command=self.modifier_utilisateur)
        self.menu.add_separator()
        self.menu.add_command(label="🗑️ Supprimer", command=self.supprimer_utilisateurs)
        self.table.bind("<Button-3>", lambda e: self._afficher_menu(e))

    def _afficher_menu(self, event):
        ligne = self.table.identify_row(event.y)
        if ligne:
            self.table.selection_set(ligne)
            self.menu.post(event.x_root, event.y_root)


# =============================================================================
#  EMPRUNTS
# =============================================================================
class Emprunt_GUI(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        header_frame, _ = creer_entete(self, "📋  Emprunts")

        # Boutons d'action dans l'entête
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        ctk.CTkButton(btn_frame, text="📋 Tous",
            command=self.afficher_emprunt,
            width=130, height=36, corner_radius=RAYON, fg_color=BLEU
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_frame, text="⚠️ Retards",
            command=self.afficher_retard,
            width=130, height=36, corner_radius=RAYON,
            fg_color=ROUGE, hover_color=ROUGE_HOVER
        ).pack(side="left")

        self._creer_barre_recherche_user()

        self.table = creer_tableau(self, {
            "nom":      ("👤 Utilisateur",  180),
            "titre":    ("📖 Livre",         240),
            "emprunt":  ("📅 Emprunté le",   130),
            "retour":   ("✅ Rendu le",       130),
            "prevue":   ("⏰ Retour prévu",   130),
        }, tag_retard=True)

        self.table.bind("<Double-1>", self.details_emprunts)
        self.afficher_emprunt()

    def _creer_barre_recherche_user(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(frame, text="Recherche par utilisateur :",
            font=(POLICE, 12, "bold")).pack(side="left", padx=(0, 12))
        self.nom    = ctk.CTkEntry(frame, placeholder_text="Nom",    width=140, height=36, corner_radius=RAYON)
        self.prenom = ctk.CTkEntry(frame, placeholder_text="Prénom", width=140, height=36, corner_radius=RAYON)
        self.nom.pack(side="left", padx=(0, 6))
        self.prenom.pack(side="left", padx=(0, 6))
        ctk.CTkButton(frame, text="🔍", command=self.afficher_recherche,
            width=38, height=36, corner_radius=RAYON, fg_color=BLEU).pack(side="left")

    def afficher_emprunt(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for b in emprunt.afficher_les_emprunts():
            self.table.insert("", "end",
                values=(b[1], b[2], b[3], b[4], b[5]),
                tags=(str(b[6]), str(b[0])))

    def afficher_retard(self):
        for item in self.table.get_children():
            self.table.delete(item)
        retards = emprunt.retard()
        if retards:
            for late in retards:
                self.table.insert("", "end",
                    values=(late[1], late[2], late[3], "⚠️ En retard !", late[4]),
                    tags=(str(late[5]), str(late[0]), "retard"))
        else:
            messagebox.showinfo("Aucun retard", "Tous les livres sont rendus à temps ✓")

    def afficher_recherche(self):
        nom    = self.nom.get().strip()
        prenom = self.prenom.get().strip()
        if not all([nom, prenom]):
            messagebox.showwarning("Champs manquants", "Nom et prénom requis !")
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
                messagebox.showinfo("Info", f"Aucun emprunt actif pour {nom} {prenom}.")
            self.nom.delete(0, "end")
            self.prenom.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def details_emprunts(self, event=None):
        selection = self.table.selection()
        if not selection:
            return
        tags    = self.table.item(selection[0], "tags")
        id_user = next((int(t) for t in tags if t.isdigit()), None)
        if id_user is None:
            return
        try:
            infos = utilisateur.afficher(id_user)
            quota = emprunt.cota_emprunt(id_user)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return

        popup = ctk.CTkToplevel(self)
        popup.title("Détails utilisateur")
        popup.geometry("480x320")
        popup.grab_set()

        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(main, text=f"👤  {infos[1]} {infos[2]}",
            font=(POLICE, 20, "bold")).pack(pady=(0, 20))

        info_card = ctk.CTkFrame(main, corner_radius=RAYON)
        info_card.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(info_card, text=f"📍  Adresse : {infos[3]}",
            font=(POLICE, 12)).pack(padx=20, pady=(16, 8), anchor="w")
        ctk.CTkLabel(info_card, text=f"📚  Emprunts actifs : {quota} / 3",
            font=(POLICE, 12, "bold")).pack(padx=20, pady=(0, 16), anchor="w")

        ctk.CTkButton(main, text="Fermer", command=popup.destroy,
            width=140, height=38, corner_radius=RAYON,
            fg_color=("gray70", "gray40")).pack()


# =============================================================================
#  EMPRUNTS EN COURS — vue utilisateur
# =============================================================================
class Emprunt_en_cours(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        creer_entete(self, "📋  Mes emprunts en cours")
        self.table = creer_tableau(self, {
            "titre":   ("📖 Livre",          340),
            "emprunt": ("📅 Emprunté le",     180),
            "prevue":  ("⏰ À rendre avant",  180),
        })
        self.afficher_emprunt()

    def afficher_emprunt(self):
        for item in self.table.get_children():
            self.table.delete(item)
        nom    = session.current_user["nom"]
        prenom = session.current_user["prenom"]
        id_user = utilisateur.retourne_id_utilisateur(nom, prenom)
        for b in emprunt.emprunt_en_cours(id_user):
            self.table.insert("", "end", values=(b[1], b[2], b[3]))


# =============================================================================
#  HISTORIQUE — vue utilisateur
# =============================================================================
class Borrow_History(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        creer_entete(self, "🕘  Historique de mes emprunts")
        self.table = creer_tableau(self, {
            "titre":    ("📖 Livre",       340),
            "emprunt":  ("📅 Emprunté le", 180),
            "rendu":    ("✅ Rendu le",     180),
        })
        self.afficher_historique()

    def afficher_historique(self):
        for item in self.table.get_children():
            self.table.delete(item)
        nom    = session.current_user["nom"]
        prenom = session.current_user["prenom"]
        id_user = utilisateur.retourne_id_utilisateur(nom, prenom)
        for h in emprunt.historique_emprunt(id_user):
            self.table.insert("", "end", values=(h[1], h[2], h[3]))


# =============================================================================
#  LOGIN
# =============================================================================
class Login_GUI:

    def __init__(self, root):
        self.parent = root
        self.parent.geometry("540x520")
        self.parent.title("Biblio — Connexion")

    def connexion(self):
        if hasattr(self, "frame") and self.frame.winfo_exists():
            self.frame.destroy()

        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=60, pady=40)

        ctk.CTkLabel(self.frame, text="📚 Biblio",
            font=(POLICE, 32, "bold"), text_color=BLEU).pack(pady=(0, 8))
        ctk.CTkLabel(self.frame, text="Connectez-vous pour continuer",
            font=(POLICE, 13), text_color=("gray50", "gray60")).pack(pady=(0, 30))

        ctk.CTkLabel(self.frame, text="Nom", font=(POLICE, 12, "bold")).pack(anchor="w")
        self.nom_entry = ctk.CTkEntry(self.frame, width=380, height=42, corner_radius=RAYON)
        self.nom_entry.pack(pady=(4, 14))

        ctk.CTkLabel(self.frame, text="Prénom", font=(POLICE, 12, "bold")).pack(anchor="w")
        self.prenom_entry = ctk.CTkEntry(self.frame, width=380, height=42, corner_radius=RAYON)
        self.prenom_entry.pack(pady=(4, 14))

        ctk.CTkLabel(self.frame, text="Mot de passe", font=(POLICE, 12, "bold")).pack(anchor="w")
        self.mdp_entry = ctk.CTkEntry(self.frame, show="*", width=380, height=42, corner_radius=RAYON)
        self.mdp_entry.pack(pady=(4, 24))

        ctk.CTkButton(self.frame, text="Se connecter",
            command=self.validation_connexion,
            width=380, height=44, corner_radius=RAYON,
            font=(POLICE, 13, "bold"), fg_color=BLEU, hover_color=BLEU_HOVER
        ).pack(pady=(0, 10))

        ctk.CTkButton(self.frame, text="Créer un compte",
            command=self.creer_compte_user,
            width=380, height=44, corner_radius=RAYON,
            font=(POLICE, 13),
            fg_color="transparent",
            border_width=1,
            text_color=(BLEU, "#7ab3ff")
        ).pack()

    def validation_connexion(self):
        nom    = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()
        mdp    = self.mdp_entry.get().strip()

        if not all([nom, prenom, mdp]):
            messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs !")
            return
        try:
            login.login(nom, prenom, mdp)
            self.frame.destroy()
            role = session.current_user["status"]
            GUI(self.parent, role=role)
        except Exception as e:
            messagebox.showerror("Connexion échouée", str(e))

    def creer_compte_user(self):
        if hasattr(self, "frame") and self.frame.winfo_exists():
            self.frame.destroy()

        self.frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=60, pady=40)

        ctk.CTkLabel(self.frame, text="Créer un compte",
            font=(POLICE, 24, "bold")).pack(pady=(0, 24))

        champs = [("Nom", False), ("Prénom", False), ("Adresse", False), ("Mot de passe", True)]
        entries = []
        for label, is_pwd in champs:
            ctk.CTkLabel(self.frame, text=label, font=(POLICE, 12, "bold")).pack(anchor="w")
            e = ctk.CTkEntry(self.frame, width=380, height=40, corner_radius=RAYON,
                show="*" if is_pwd else "")
            e.pack(pady=(4, 12))
            entries.append(e)

        def valider():
            nom, prenom, adresse, mdp = [e.get().strip() for e in entries]
            if not all([nom, prenom, adresse, mdp]):
                messagebox.showwarning("Champs vides", "Tous les champs sont requis !")
                return
            try:
                login.creer_compte_user(nom, prenom, adresse, mdp)
                messagebox.showinfo("Compte créé", f"Bienvenue {prenom} {nom} !")
                self.frame.destroy()
                GUI(self.parent, role="user")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        ctk.CTkButton(self.frame, text="S'inscrire", command=valider,
            width=380, height=44, corner_radius=RAYON,
            font=(POLICE, 13, "bold"), fg_color=BLEU, hover_color=BLEU_HOVER
        ).pack(pady=(8, 10))

        ctk.CTkButton(self.frame, text="J'ai déjà un compte", command=self.connexion,
            width=380, height=44, corner_radius=RAYON,
            font=(POLICE, 13),
            fg_color="transparent", border_width=1,
            text_color=(BLEU, "#7ab3ff")
        ).pack()


# =============================================================================
#  LANCEMENT
# =============================================================================
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app  = Login_GUI(root)
    app.connexion()
    root.mainloop()