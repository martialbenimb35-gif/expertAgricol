import os
from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('MYSQLHOST'),
        user=os.environ.get('MYSQLUSER'),
        password=os.environ.get('MYSQLPASSWORD'),
        database=os.environ.get('MYSQLDATABASE'),
        port=int(os.environ.get('MYSQLPORT', 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    # 1. On initialise toujours les variables à None (Réinitialisation)
    diagnostic = None
    solution = None
    symptomes = []

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 2. On récupère la liste des symptômes pour le menu déroulant
            cursor.execute("SELECT DISTINCT symptome FROM rules")
            symptomes = cursor.fetchall()

            # 3. On ne cherche le résultat QUE si l'utilisateur a cliqué sur le bouton
            if request.method == 'POST':
                selected_symptome = request.form.get('symptome')
                if selected_symptome:
                    sql = "SELECT diagnostic, solution FROM rules WHERE symptome = %s"
                    cursor.execute(sql, (selected_symptome,))
                    result = cursor.fetchone()
                    if result:
                        diagnostic = result['diagnostic']
                        solution = result['solution']
        connection.close()
    except Exception as e:
        print(f"Erreur de connexion : {e}")

    # 4. On envoie les données au HTML
    # Si c'est un GET (rafraîchissement), diagnostic et solution seront None
    return render_template('index.html', 
                           symptomes=symptomes, 
                           diagnostic=diagnostic, 
                           solution=solution)

if __name__ == '__main__':
    app.run(debug=True)