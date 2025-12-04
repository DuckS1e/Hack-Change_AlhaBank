from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
#custom_path = '/Users/maksserdukov/Desktop/Учеба/Без названия/public'
app = Flask(__name__, template_folder='../public')
app.secret_key = 'ekwlnkfejwopJKNB98#@'


def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/client')
def client():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('client.html')


@app.route('/analysis')
def analysis():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('analysis.html')


@app.route('/offers')
def offers():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('offers.html')


@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmation = request.form['confirm_password']

        if password != confirmation:
            flash('Пароли не совпали twin')
            return render_template('register.html')

        hash_pass = generate_password_hash(password)

        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                      (username, email, hash_pass))
            conn.commit()
            conn.close()
            flash('Регистрация успешна cuhh проходи nigga')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Такой brototype уже есть')
            return render_template('register.html')
        except Exception as e:
            flash(f'Произошла ошибка: {str(e)}')
            return render_template('register.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if not username or not password:
            flash('Заполните все поля!')
        else:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            conn.close()

            if user and check_password_hash(user[3], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                flash('Вход выполнен успешно!')
                return redirect(url_for('home'))
            else:
                flash('Неверное имя пользователя или пароль!')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)