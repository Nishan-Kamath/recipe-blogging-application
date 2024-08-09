
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def connect_db():
    conn = sqlite3.connect('dishdazzle.db')
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    error_message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            error_message = 'Please fill in all fields.'
        else:
            user = get_user(username, password)
            if user:
                session['username'] = username  # Store the username in the session
                return redirect(url_for('dashboard', first_char=username))
            else:
                error_message = 'Invalid username or password.'
    return render_template('login.html', error_message=error_message)

@app.route('/dashboard/<first_char>')
def dashboard(first_char):
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', first_char=first_char, username=username)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def get_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error_message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        bio = request.form['bio']

        if not username or not password or not bio:
            error_message = 'Please fill in all fields.'
        else:
            if not is_user_exists(username):
                add_user(username, password, bio)
                return redirect(url_for('login')) 
            else:
                error_message = 'Username already exists.'
    return render_template('signup.html', error_message=error_message)

def add_user(username, password, bio):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (username, password, bio) VALUES (?, ?, ?)",
                   (username, password, bio))
    conn.commit()
    conn.close()

def is_user_exists(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

@app.route('/profile/<username>')
def profile(username):
    user = get_user_by_username(username)
    if user:
        recipes = get_recipes_by_user(username)
        if 'username' in session:
            username = session['username']
            return render_template('profile.html', user=user, recipes=recipes)
    else:
        return "User not found", 404

def get_recipes_by_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipe WHERE user = ?", (username,))
    recipes = cursor.fetchall()
    conn.close()
    return recipes

def get_user_by_username(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/render_category_page/<category>')
def render_category_page(category):
    recipes = get_recipes_by_category(category)
    return render_template('category.html', category=category, recipes=recipes)

def get_recipes_by_category(category):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipe WHERE category = ?", (category,))
    recipes = cursor.fetchall()
    conn.close()
    return recipes

@app.route('/post_recipe', methods=['POST'])
def post_recipe():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            recipe_name = request.form['recipe_name']
            category = request.form['category']
            ingredients = request.form['ingredients']
            steps = request.form['steps']
            save_recipe_to_database(username, recipe_name, category, ingredients, steps)

            return redirect(url_for('profile', username=username))
        else:
            return redirect(url_for('login'))

def save_recipe_to_database(username, recipe_name, category, ingredients, steps):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipe (user, recipe_name, category, ingredients, steps) VALUES (?, ?, ?, ?, ?)",
                   (username, recipe_name, category, ingredients, steps))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
