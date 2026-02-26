from controleurBiblio import Book_Manager, Author_Manager

# Initialisation des gestionnaires
livres = Book_Manager("test01.db")
# Note : Ton code utilise Author_Manager mais l'appel se fait via livres.ajouter_livre
# On l'initialise au cas où ton contrôleur en ait besoin en arrière-plan
auteur = Author_Manager("test01.db")

livres_test = [
    # Classiques & Littérature
    ("1984", "George Orwell", 1903, "Royaume-Uni", "Disponible", 1949, 5, "Dystopie"),
    ("Le Petit Prince", "Antoine de Saint-Exupéry", 1900, "France", "Disponible", 1943, 3, "Conte"),
    ("Harry Potter à l'école des sorciers", "J.K. Rowling", 1965, "Royaume-Uni", "Emprunté", 1997, 2, "Fantasy"),
    ("Les Misérables", "Victor Hugo", 1802, "France", "Disponible", 1862, 4, "Classique"),
    ("L'Étranger", "Albert Camus", 1913, "Algérie", "Disponible", 1942, 6, "Philosophie"),
    ("Le Vieil Homme et la Mer", "Ernest Hemingway", 1899, "USA", "Disponible", 1952, 3, "Aventure"),
    ("Guerre et Paix", "Léon Tolstoï", 1828, "Russie", "Disponible", 1869, 2, "Historique"),
    ("Orgueil et Préjugés", "Jane Austen", 1775, "Royaume-Uni", "Disponible", 1813, 5, "Romance"),
    ("Faust", "Johann Wolfgang von Goethe", 1749, "Allemagne", "Disponible", 1808, 2, "Drame"),
    ("Don Quichotte", "Miguel de Cervantes", 1547, "Espagne", "Disponible", 1605, 3, "Classique"),
    
    # Science-Fiction & Fantastique
    ("Dune", "Frank Herbert", 1920, "USA", "Disponible", 1965, 4, "SF"),
    ("Fondation", "Isaac Asimov", 1920, "Russie", "Disponible", 1951, 5, "SF"),
    ("Le Seigneur des Anneaux", "J.R.R. Tolkien", 1892, "Royaume-Uni", "Disponible", 1954, 3, "Fantasy"),
    ("Fahrenheit 451", "Ray Bradbury", 1920, "USA", "Disponible", 1953, 4, "Dystopie"),
    ("Neuromancien", "William Gibson", 1948, "USA", "Disponible", 1984, 2, "Cyberpunk"),
    ("Le Meilleur des Mondes", "Aldous Huxley", 1894, "Royaume-Uni", "Disponible", 1932, 5, "Dystopie"),
    ("Ubik", "Philip K. Dick", 1928, "USA", "Emprunté", 1969, 3, "SF"),
    ("Chroniques Martiennes", "Ray Bradbury", 1920, "USA", "Disponible", 1950, 4, "SF"),
    ("Le Sorceleur", "Andrzej Sapkowski", 1948, "Pologne", "Disponible", 1990, 6, "Fantasy"),
    ("La Horde du Contrevent", "Alain Damasio", 1969, "France", "Disponible", 2004, 3, "Fantasy"),

    # Policier & Thriller
    ("Dix Petits Nègres", "Agatha Christie", 1890, "Royaume-Uni", "Disponible", 1939, 8, "Policier"),
    ("Sherlock Holmes", "Arthur Conan Doyle", 1859, "Royaume-Uni", "Disponible", 1887, 5, "Policier"),
    ("Millénium", "Stieg Larsson", 1954, "Suède", "Disponible", 2005, 4, "Thriller"),
    ("Le Nom de la Rose", "Umberto Eco", 1932, "Italie", "Disponible", 1980, 2, "Historique"),
    ("Da Vinci Code", "Dan Brown", 1964, "USA", "Emprunté", 2003, 7, "Thriller"),
    ("Le Silence des Agneaux", "Thomas Harris", 1940, "USA", "Disponible", 1988, 3, "Thriller"),
    ("Gone Girl", "Gillian Flynn", 1971, "USA", "Disponible", 2012, 4, "Thriller"),
    ("La Fille du Train", "Paula Hawkins", 1972, "Zimbabwe", "Disponible", 2015, 5, "Thriller"),
    ("Le Poète", "Michael Connelly", 1956, "USA", "Disponible", 1996, 3, "Policier"),
    ("Pars vite et reviens tard", "Fred Vargas", 1957, "France", "Disponible", 2001, 4, "Policier"),

    # Littérature Contemporaine & Divers
    ("L'Alchimiste", "Paulo Coelho", 1947, "Brésil", "Disponible", 1988, 10, "Conte"),
    ("La Vérité sur l'affaire Harry Quebert", "Joël Dicker", 1985, "Suisse", "Disponible", 2012, 4, "Policier"),
    ("Kilomètre Zéro", "Maud Ankaoua", 1971, "France", "Disponible", 2017, 3, "Développement"),
    ("Sapiens", "Yuval Noah Harari", 1976, "Israël", "Disponible", 2011, 5, "Essai"),
    ("L'Anomalie", "Hervé Le Tellier", 1957, "France", "Disponible", 2020, 4, "Roman"),
    ("Petit Pays", "Gaël Faye", 1982, "Burundi", "Disponible", 2016, 3, "Roman"),
    ("L'Amie Prodigieuse", "Elena Ferrante", 1943, "Italie", "Disponible", 2011, 6, "Drame"),
    ("En attendant Bojangles", "Olivier Bourdeaut", 1980, "France", "Disponible", 2016, 4, "Roman"),
    ("Changer l'eau des fleurs", "Valérie Perrin", 1967, "France", "Disponible", 2018, 5, "Roman"),
    ("Le Chardonneret", "Donna Tartt", 1963, "USA", "Disponible", 2013, 2, "Roman"),

    # Philosophie & Réflexion
    ("Ainsi parlait Zarathoustra", "Friedrich Nietzsche", 1844, "Allemagne", "Disponible", 1883, 2, "Philosophie"),
    ("Méditations", "Marc Aurèle", 121, "Rome", "Disponible", 180, 4, "Philosophie"),
    ("Le Banquet", "Platon", -427, "Grèce", "Disponible", -380, 3, "Philosophie"),
    ("Candide", "Voltaire", 1694, "France", "Disponible", 1759, 5, "Conte"),
    ("Le Prince", "Nicolas Machiavel", 1469, "Italie", "Disponible", 1532, 3, "Politique"),
    ("L'Art de la Guerre", "Sun Tzu", -544, "Chine", "Disponible", -500, 6, "Stratégie"),
    ("Une chambre à soi", "Virginia Woolf", 1882, "Royaume-Uni", "Disponible", 1929, 4, "Essai"),
    ("La Condition humaine", "André Malraux", 1901, "France", "Disponible", 1933, 3, "Roman"),
    ("Bel-Ami", "Guy de Maupassant", 1850, "France", "Disponible", 1885, 4, "Classique"),
    ("Madame Bovary", "Gustave Flaubert", 1821, "France", "Disponible", 1857, 3, "Classique")
]

print(f"--- Début de l'importation (Cible : {len(livres_test)} livres) ---")

compteur = 0
for titre, auteur_nom, date_auteur, pays, etat, date_livre, qte, genre in livres_test:
    try:
        livres.ajouter_livre(titre, auteur_nom, date_auteur, pays, etat, date_livre, qte, genre)
        compteur += 1
        print(f"[{compteur}/50] ✓ {titre}")
    except Exception as e:
        print(f"✗ Erreur pour {titre}: {e}")

print(f"\nTerminé ! {compteur} livres ont été ajoutés à test01.db.")