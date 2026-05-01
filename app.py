from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)


def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',     
        password='',      # Ton mot de passe (vide par défaut sur XAMPP)
        database='agri_db',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    connection = get_db_connection()
    resultat = None
    
    try:
        with connection.cursor() as cursor:
            # 1. Charger toutes les règles pour remplir la liste déroulante
            cursor.execute("SELECT * FROM rules")
            base_regles = cursor.fetchall()

            if request.method == 'POST':
                symptome_choisi = request.form.get('symptome')
                # 2. Moteur d'inférence : Chercher le diagnostic dans la BDD
                sql = "SELECT * FROM rules WHERE symptome = %s"
                cursor.execute(sql, (symptome_choisi,))
                resultat = cursor.fetchone()
    finally:
        connection.close()
    
    return render_template('index.html', regles=base_regles, resultat=resultat)

if __name__ == '__main__':
    app.run(debug=True)
    