from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # Nécessaire pour utiliser flash messages

# Fonction pour établir la connexion à la base de données
def creer_connexion():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Atanima3026@',
            database='magasin',
        )
        return conn
    except Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None

# Page de bienvenue avec instructions
@app.route('/')
def bienvenue():
    message = "Bienvenue! Utilisez le menu pour ajouter ou gérer des produits et fournisseurs."
    return render_template('bienvenue.html', message=message)

# Afficher tous les produits
@app.route('/produit')
def afficher_produits():
    conn = creer_connexion()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produit")
        produit = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('produit.html', produit=produit)
    else:
        flash("Erreur de connexion à la base de données.")
        return redirect(url_for('bienvenue'))

# Ajouter un produit
@app.route('/ajouterproduit', methods=['GET', 'POST'])
def ajouterproduit():
    if request.method == 'POST':
        nom = request.form['nom']
        prix = request.form['prix']
        stock = request.form['stock']
        conn = creer_connexion()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Produit (nom, prix, stock) VALUES (%s, %s, %s)", (nom, prix, stock))
                conn.commit()
                flash("Produit ajouté avec succès.")
            except Error as e:
                conn.rollback()
                flash(f"Erreur : {e}")
            finally:
                conn.close()
            return redirect(url_for('afficher_produits'))
    return render_template('ajouterproduit.html')

# Modifier un produit
@app.route('/produit/modifierproduit/<int:produit_id>', methods=['GET', 'POST'])
def modifierproduit(produit_id):
    conn = creer_connexion()
    if conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            nom = request.form['nom']
            prix = request.form['prix']
            stock = request.form['stock']
            try:
                cursor.execute("UPDATE Produit SET nom=%s, prix=%s, stock=%s WHERE id=%s", (nom, prix, stock, produit_id))
                conn.commit()
                flash("Produit mis à jour avec succès.")
            except Error as e:
                conn.rollback()
                flash(f"Erreur : {e}")
            finally:
                conn.close()
            return redirect(url_for('afficher_produits'))
        cursor.execute("SELECT * FROM Produit WHERE id = %s", (produit_id,))
        produit = cursor.fetchone()
        conn.close()
        return render_template('modifierproduit.html', produit=produit)

# Supprimer un produit
@app.route('/produit/supprimerproduit/<int:produit_id>')
def supprimerproduit(produit_id):
    conn = creer_connexion()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Produit WHERE id = %s", (produit_id,))
            conn.commit()
            flash("Produit supprimé avec succès.")
        except Error as e:
            conn.rollback()
            flash(f"Erreur : {e}")
        finally:
            conn.close()
    return redirect(url_for('afficher_produits'))

# Afficher tous les fournisseurs
@app.route('/fournisseurs')
def afficher_fournisseurs():
    conn = creer_connexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Fournisseur")
        fournisseurs = cursor.fetchall()
        conn.close()
        return render_template('fournisseurs.html', fournisseurs=fournisseurs)
    else:
        flash("Erreur de connexion à la base de données.")
        return redirect(url_for('bienvenue'))

# Enregistrer une vente et mettre à jour le stock
@app.route('/ajouterventes', methods=['GET', 'POST'])
def enregistrer_vente():
    if request.method == 'POST':
        produit_id = request.form['produit_id']
        quantite = int(request.form['quantite'])
        conn = creer_connexion()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT stock FROM Produit WHERE id = %s", (produit_id,))
                stock_actuel = cursor.fetchone()[0]
                if stock_actuel >= quantite:
                    cursor.execute("INSERT INTO Vente (produit_id, quantite) VALUES (%s, %s)", (produit_id, quantite))
                    cursor.execute("UPDATE Produit SET stock = stock - %s WHERE id = %s", (quantite, produit_id))
                    conn.commit()
                    flash("Vente enregistrée avec succès et stock mis à jour.")
                else:
                    flash("Stock insuffisant pour cette vente.")
            except Error as e:
                conn.rollback()
                flash(f"Erreur : {e}")
            finally:
                conn.close()
            return redirect(url_for('afficher_produits'))
    return render_template('ajouterventes.html')

if __name__ == '__main__':
    app.run(debug=True)