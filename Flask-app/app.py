import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# === Умное определение путей ===
def find_public_folder():
    # Пути, где может быть папка public
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "public"),           # ./public (рядом с app.py)
        os.path.join(os.path.dirname(__file__), "..", "public"),     # ../public (на уровень выше)
        "public",                                                    # В текущей директории
    ]
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path) and os.path.isdir(abs_path):
            print(f"✅ Найдена папка public: {abs_path}")
            return abs_path
    raise Exception("❌ Не найдена папка 'public'. Проверьте структуру проекта.")

# === Определяем пути ===
try:
    PUBLIC_DIR = find_public_folder()
    STATIC_DIR = os.path.join(PUBLIC_DIR, "static")
except Exception as e:
    print(e)
    exit(1)

# Проверим, есть ли static
if not os.path.exists(STATIC_DIR):
    print(f"⚠️  Папка static не найдена: {STATIC_DIR}")
    print("Создаю пустую папку (но стили работать не будут)")
    os.makedirs(STATIC_DIR, exist_ok=True)

app = Flask(
    __name__,
    template_folder=PUBLIC_DIR,           # HTML
    static_folder=STATIC_DIR,             # CSS, JS, IMG
    static_url_path="/static"             # URL: /static/css/style.css
)

app.secret_key = 'ekwlnkfejwopJKNB98#@'

# === Для отладки — выводим пути при запуске ===
print(f"🌍 Запуск приложения...")
print(f"📁 Шаблоны: {app.template_folder}")
print(f"📦 Статика:  {app.static_folder}")
print(f"🔗 Статик URL: {app.static_url_path}")

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