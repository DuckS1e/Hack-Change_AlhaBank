from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
app = Flask(__name__)
app.secret_key = 'ekwlnkfejwopJKNB98#@'
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', username=session.get('username'))
    return redirect(url_for('login'))

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmation = request.form['confirmation']
        if password != confirmation:
            flash('Пароли не совпали twin')
            return render_template('reg.html')

        hash_pass = generate_password_hash(password)

        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("""INSERT INTO users (username, email, password) VALUES (?, ?, ?)"""), (username, email, hash_pass)
            conn.commit()
            conn.close()
            flash('Регистрация успешна cuhh проходи nigga')
            return redirect(url_for('login'))
        except:
            flash('Такой brototype уже есть')

        return render_template('reg.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM users WHERE USERNAME = ?""", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['email'] = user[2]
            flash('Вход выполнен успешно')
            return redirect(url_for('index'))
        else:
            flash('Ты ошибся cuh')

        render_template('log.html')


@app.route('/logout')
def logout():
    session.pop('user_id')
    session.pop('username')
    session.pop('email')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)