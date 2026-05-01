import os
import pymysql
from flask import Flask, render_template, request

app = Flask(__name__)

# --- CONFIGURATION DE LA CONNEXION ---
def get_db_connection():
    # os.environ.get récupère les variables "violettes" que tu as mises sur Railway
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
    diagnostic = None
    solution = None
    selected_symptome = None

    # Connexion à la base pour récupérer la liste des symptômes
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT symptome FROM rules")
            symptomes = cursor.fetchall()

            if request.method == 'POST':
                selected_symptome = request.form.get('symptome')
                # Recherche du diagnostic correspondant
                cursor.execute("SELECT diagnostic, solution FROM rules WHERE symptome = %s", (selected_symptome,))
                result = cursor.fetchone()
                if result:
                    diagnostic = result['diagnostic']
                    solution = result['solution']
    finally:
        connection.close()

    return render_template('index.html', 
                           symptomes=symptomes, 
                           diagnostic=diagnostic, 
                           solution=solution, 
                           selected_symptome=selected_symptome)

if __name__ == '__main__':
    # TRÈS IMPORTANT pour Railway : utiliser le port donné par l'environnement
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)