# Connect to SQLite database
import sqlite3
conn = sqlite3.connect('dishdazzle.db')
cursor = conn.cursor()
"""
# Create user table with bio column
cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                    username TEXT primary key,
                    password TEXT,
                    bio TEXT
                )''')


cursor.execute('''create table if not exists recipe(
                    user text,
                    recipe_name text,
                    category text,
                    ingredients text,
                    steps text,
                    FOREIGN KEY (user) REFERENCES user(username))'''
)"""

"""result = cursor.execute('select * from recipe').fetchall()
for i in result:
    print(i)
print('-----------------------------')
result = cursor.execute('select * from recipe where category="salad"').fetchall()
for i in result:
    print(i)"""
def get_recipes_by_category(category):
    cursor.execute("SELECT * FROM recipe WHERE category = ?", (category,))
    recipes = cursor.fetchall()
    return recipes

category = 'dessert'
recipes = get_recipes_by_category(category)
for i in recipes:
    print(i)

#cursor.execute('delete from recipe where recipe_name = "samosa"')
# Commit changes and close connection
conn.commit()
conn.close()