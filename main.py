from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector
import pandas as pd

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # Use your MySQL server's host
        user="root",  # Use your MySQL username
        password="root",  # Use your MySQL password
        database="sample_app"
    )

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM people WHERE name = %s', (name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return redirect(url_for('details', name=name))
    return render_template('home.html')

@app.route('/details/<name>')
def details(name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM people WHERE name = %s', (name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        df = pd.DataFrame([result])
        df.to_excel('details.xlsx', index=False)
        return render_template('details.html', name=name)
    else:
        return redirect(url_for('home'))

@app.route('/download/<name>')
def download(name):
    return send_file('details.xlsx', as_attachment=True, download_name=f'{name}_details.xlsx')


if __name__ == '__main__':
    app.run(debug=True)
