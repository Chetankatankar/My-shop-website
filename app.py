from flask import Flask, render_template, request, redirect, session
import mysql.connector
from urllib.parse import urlparse
import os

# object for Flask class
app = Flask(__name__)
app.secret_key = "chetan"

# Database connection setup
db_url = os.getenv("DATABASE_URL")

if db_url:
    # Parse database URL from Railway
    url = urlparse(db_url)
    cnx = mysql.connector.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path[1:],  # remove leading slash
        port=url.port
    )
else:
    # Fallback for local development
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="chetan",
        database="shop"
    )

# Cursor object
cur = cnx.cursor()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/getdata", methods=['POST'])
def getdata():
    user_name = request.form['user_name']
    phone_no = request.form['phone_no']
    password = request.form['password']
    q = "INSERT INTO register (user_name, phone_no, password) VALUES (%s, %s, %s)"
    cur.execute(q, (user_name, phone_no, password))
    cnx.commit()
    return redirect('/login')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/check', methods=['POST'])
def check():
    user_name = request.form['user_name']
    password = request.form['password']
    q = "SELECT * FROM register WHERE user_name=%s AND password=%s"
    cur.execute(q, (user_name, password))
    res = cur.fetchone()
    if res is None:
        return "User doesn't exist or phone number or password is incorrect!"    
    session['loggedIn'] = True
    session['user_name'] = res[1]
    session['password'] = res[3]
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/category')
def category():
    q = "SELECT * FROM categories"
    cur.execute(q)
    res = cur.fetchall()
    return render_template('category.html', categories=res)

@app.route("/view_by_category", methods=['POST'])
def view_by_category():
    category = request.form['category']
    q = "SELECT * FROM categories WHERE image_category LIKE %s"
    cur.execute(q, ('%' + category + '%',))
    res = cur.fetchall()
    return render_template("view_category.html", res=res)

@app.route("/shop")
def shop():
    return render_template('shop.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/get_message", methods=['POST'])
def get_message():
    name = request.form['name']
    phone_no = request.form['phone_no']
    message = request.form['message']
    q = "INSERT INTO contact (name, phone_no, message) VALUES(%s, %s, %s)"
    cur.execute(q, (name, phone_no, message))
    cnx.commit()
    return redirect('/contact_message')

@app.route('/contact_message')
def contact_message():
    return render_template('contact_message.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
