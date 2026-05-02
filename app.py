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
    diagnostic = None
    solution = None
    symptomes = []

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Récupération des symptômes
            cursor.execute("SELECT DISTINCT symptome FROM rules")
            symptomes = cursor.fetchall()

            # Si on clique sur le bouton
            if request.method == 'POST':
                selected = request.form.get('symptome')
                if selected:
                    cursor.execute("SELECT diagnostic, solution FROM rules WHERE symptome = %s", (selected,))
                    result = cursor.fetchone()
                    if result:
                        diagnostic = result['diagnostic']
                        solution = result['solution']
        connection.close()
    except Exception as e:
        print(f"ERREUR : {e}")

   # Remplace symptomes=symptomes par regles=symptomes
    return render_template('index.html', 
                       regles=symptomes, 
                       diagnostic=diagnostic, 
                       solution=solution)