from flask import Flask, request, jsonify, session, render_template, send_from_directory
import mysql.connector
import os

app = Flask(__name__)

# Configurazione database
db_config = {
    'host': 'mysql-3c32f481-filippopietro-5cb4.l.aivencloud.com',
    'user': 'avnadmin',
    'password': os.environ['DB_PASSWORD'],
    'database': 'W3Schools', 
    'port': 18611
}

# Funzione di connessione al database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# visualizzazione dati tabella
@app.route('/show1/<string:tableName>/<int:numRows>', methods=['GET'])
def get_table_data(tableName, numRows):

    # Parametri inseriti nell'URL:
    # https://5000-wtitze-spaesempi-mcjzwsnbq0z.ws-eu117.gitpod.io/show1/Categories/4

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"""
        SELECT *
        FROM {tableName}
        LIMIT {numRows}
    """)
    result = cursor.fetchall()
    conn.close()

    return jsonify(result)

@app.route('/show2', methods=['GET', 'POST'])
def table_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'GET':

        # Parametri passati come query string
        # https://5000-wtitze-spaesempi-mcjzwsnbq0z.ws-eu117.gitpod.io/show2?tableName=Categories&numRows=3

        table_name = request.args.get('tableName')
        num_rows = int(request.args.get('numRows', 10))  # Default a 10 righe se non specificato

    elif request.method == 'POST':

        # Parametri inseriti nel body in formato JSON:
        # {
        #    "tableName": "Categories",
        #    "numRows": 3
        # }

        data = request.json
        table_name = data.get('tableName')
        num_rows = data.get('numRows', 10)  # Default a 10 righe se non specificato

    # Query 
    query = f"""
        SELECT *
        FROM {table_name}
        LIMIT {num_rows}
    """
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    return jsonify(result)

@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        
        # Parametri inseriti nell'URL:
        # https://5000-wtitze-spaesempi-mcjzwsnbq0z.ws-eu117.gitpod.io
        # /add-category?CategoryName=Apparel&
        # Description=Clothing, including shirts, pants, and accessories

        category_name = request.args.get('CategoryName')
        description = request.args.get('Description')

    elif request.method == 'POST':

        # Parametri inseriti nel body in formato JSON:
        # {
        #    "CategoryName": "Snacks",
        #    "Description": "Quick bites"
        # }

        data = request.json
        category_name = data.get('CategoryName')
        description = data.get('Description')

    # Inserimento nel database
    query = f"""
        INSERT INTO Categories (CategoryName, Description)
        VALUES ('{category_name}', '{description}')
    """
    cursor.execute(query)
    conn.commit() # importante, senza non inserisce i dati nella tabella

    # Ottieni l'ID della nuova categoria
    new_category_id = cursor.lastrowid
    conn.close()

    # Restituisci i dettagli della nuova categoria
    return jsonify({
        "CategoryID": new_category_id,
        "CategoryName": category_name,
        "Description": description
    }), 201

if __name__ == '__main__':
    app.run(debug=True)