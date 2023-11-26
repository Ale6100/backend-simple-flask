from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

variables_database = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password':os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}

app = Flask(__name__)

frontends_enabled = [os.getenv('URL_FRONTEND1')]

CORS(app, resources={r"/*": {"origins": frontends_enabled}}) # Permite peticiones desde los frontends de la lista

class Database: # Creamos una clase para iniciar la base de datos
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password
        )
        self.cursor = self.conn.cursor()

        if self.conn.is_connected():
            print("Base de datos conectada")
        else:
            raise Exception("No se pudo conectar a la base de datos")

        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err
        
        # Crea la tabla reviews si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            country VARCHAR(50) NOT NULL,
            image VARCHAR(255) NOT NULL,
            review VARCHAR(255) NOT NULL,
            score DECIMAL(10,2) NOT NULL,
            author VARCHAR(50) NOT NULL,
            date VARCHAR(50) NOT NULL
            )
            ''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

db = Database(**variables_database) # Se conecta a la base de datos

class Reviews(): # Creamos esta clase para interactuar con la tabla reviews
    def __init__(self, db: Database): # Se asocia con la base de datos que le pasemos como parámetro
        self.db = db

    def get_all(self): # Retorna todos los registros de la tabla
        self.db.cursor.execute("SELECT * FROM reviews")
        reviews = self.db.cursor.fetchall()
        return reviews
    
    def insert_one(self, title: str, country: str, image: str, review: str, score: int, author: str, date: str): # Inserta un solo registro
        sql = "INSERT INTO reviews (title, country, image, review, score, author, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (title, country, image, review, score, author, date)
        self.db.cursor.execute(sql, values)
        self.db.conn.commit()
        return True
    
reviews = Reviews(db)

@app.route('/', methods=['GET']) # Una pequeña bienvenida en la ruta raíz
def index():
    return '''
    <h1>API simple</h1>
    <p>Bienvenido a mi primera API con Flask. Este es el único endpoint público</p>
    ''', 200

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    try:
        return jsonify({'status': 'success', 'data': reviews.get_all()}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'error': f'{e}'}), 500

@app.route('/api/reviews', methods=['POST'])
def post_review():
    try:
        title = request.json.get('title')
        country = request.json.get('country')
        image = request.json.get('image')
        review = request.json.get('review')
        score = request.json.get('score')
        author = request.json.get('author')
        date = datetime.now().date()

        if not title or not country or not image or not review or not isinstance(score, (int, float)) or not author:
            return jsonify({'status': 'error', 'message': 'Missing data'}), 400

        reviews.insert_one(title, country, image, review, score, author, date)
        return jsonify({'status': 'success', 'message': 'Review added'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'error': f'{e}'}), 500
