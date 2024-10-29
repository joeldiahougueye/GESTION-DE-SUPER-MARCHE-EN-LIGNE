import mysql.connector
from mysql.connector import Error, errorcode


    # établir la connexion à la base de données
conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Atanima3026@',
        database='magasin',
        raise_on_warnings=True
    )
cursor = conn.cursor()

# créer les tables produit, vente et fournisseur
def creer_tables():
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produit (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100) NOT NULL,
            prix DECIMAL(10, 2) NOT NULL,
            stock INT NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Fournisseur (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100) NOT NULL,
            contact VARCHAR(100)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vente (
            id INT AUTO_INCREMENT PRIMARY KEY,
            produit_id INT,
            quantite INT,
            date_vente DATETIME DEFAULT NOW(),
            FOREIGN KEY (produit_id) REFERENCES Produit(id)
        );
        """)
        conn.commit()
        print("Tables créées avec succès.")

# Insérer un produit et un fournisseur avec gestion de transaction
def inserer_produit(nom, prix, stock):
        try:
            cursor.execute("INSERT INTO Produits (nom, prix, stock) VALUES (%s, %s, %s)", (nom, prix, stock))
            conn.commit()
            print(f"Produit {nom} inséré avec succès.")
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Erreur : {err}")

def inserer_fournisseur(nom, contact):
        try:
            cursor.execute("INSERT INTO Fournisseurs (nom, contact) VALUES (%s, %s)", (nom, contact))
            conn.commit()
            print(f"Fournisseur {nom} inséré avec succès.")
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Erreur : {err}")

# afficher les produits avec les informations de stock
def afficher_produits():
        cursor.execute("SELECT * FROM Produits")
        resultats = cursor.fetchall()
        for produit in resultats:
            print(f"ID: {produit[0]}, Nom: {produit[1]}, Prix: {produit[2]}, Stock: {produit[3]}")

    # Enregistrer une vente et mettre à jour le stock avec gestion de transaction 
def enregistrer_vente(produit_id, quantite):
    try:
            cursor.execute("SELECT stock FROM Produits WHERE id = %s", (produit_id,))
            stock_actuel = cursor.fetchone()[0]
            if stock_actuel >= quantite:
                cursor.execute("INSERT INTO Ventes (produit_id, quantite) VALUES (%s, %s)", (produit_id, quantite))
                cursor.execute("UPDATE Produits SET stock = stock - %s WHERE id = %s", (quantite, produit_id))
                conn.commit()
                print("Vente enregistrée avec succès et stock mis à jour.")
            else:
                print("Stock insuffisant pour cette vente.")
    except mysql.connector.Error as err:
            conn.rollback()
            print(f"Erreur : {err}")

 # Créer une procédure stockée pour augmenter le stock d’un produit
def creer_procedure_augmenter_stock():
        try:
            cursor.execute("""
            CREATE PROCEDURE AugmenterStock(IN prod_id INT, IN ajout INT)
            BEGIN
                UPDATE Produits SET stock = stock + ajout WHERE id = prod_id;
            END;
            """)
            conn.commit()
            print("Procédure stockée créée avec succès.")
        except mysql.connector.Error as err:
            print(f"Erreur de création de procédure : {err}")

    # Appeler la procédure stockée
def appeler_procedure_augmenter_stock(produit_id, ajout):
        try:
            cursor.callproc('AugmenterStock', [produit_id, ajout])
            conn.commit()
            print(f"Stock augmenté de {ajout} pour le produit ID {produit_id}.")
        except mysql.connector.Error as err:
            print(f"Erreur d'exécution de la procédure : {err}")

    # Supprimer un produit avec gestion de transaction
def supprimer_produit(produit_id):
        try:
            cursor.execute("DELETE FROM Produits WHERE id = %s", (produit_id,))
            conn.commit()
            print(f"Produit avec ID {produit_id} supprimé avec succès.")
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Erreur lors de la suppression : {err}")

 # Mettre à jour un produit

def modifier_produit(produit_id, nouveau_prix, nouveau_stock):
        try:
            cursor.execute("UPDATE Produits SET prix = %s, stock = %s WHERE id = %s", (nouveau_prix, nouveau_stock, produit_id))
            conn.commit()
            print(f"Produit avec ID {produit_id} mis à jour avec succès.")
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Erreur lors de la mise à jour : {err}")

    # Exécution des fonctions

creer_tables()
inserer_produit("Laptop", 1500.00, 10)
inserer_fournisseur("Fournisseur A", "contact@fournisseura.com")
afficher_produits()
enregistrer_vente(1, 2)
creer_procedure_augmenter_stock()
appeler_procedure_augmenter_stock(1, 5)
modifier_produit(1, 1400.00, 20)   # Met à jour le produit avec un nouveau prix et un nouveau stock
supprimer_produit(1)               # Supprime le produit avec l'ID 1
afficher_produits()

# fermer la connexion

cursor.close()
conn.close()
print("Connexion fermée.")

