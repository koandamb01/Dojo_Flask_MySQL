from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL # import the function connectToMySQL from the file mysqlconnection.py
import re, datetime
from datetime import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "2pacshakur"

# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
ZIPCODE_REGEX = re.compile(r'^([0-9]){5}(([ ]|[-])?([0-9]){4})?$')
WORD_SPACE_REGEX = re.compile(r'^[A-Za-z ]+')


# mysql = connectToMySQL('advanced_login_DB')
# query = 'SELECT * FROM users WHERE username = %(username)s'
# result = mysql.query_db(query, data)

@app.route('/users')
def home():
    mysql = connectToMySQL('CRUD_DB')
    users_list = mysql.query_db('SELECT id, first_name, last_name, email, DATE_FORMAT(created_at, "%M %D, %Y") AS created_at FROM users;')
    return render_template('home.html', users_list=users_list)

@app.route('/users/new')
def new():
    return render_template('new.html')

@app.route('/users/show')
def show():
    return render_template('show.html')

@app.route('/edit/<id>')
def edit(id):
    data = {'id': id}
    mysql = connectToMySQL('CRUD_DB')
    query = 'SELECT * FROM users WHERE id = %(id)s'
    user = mysql.query_db(query, data)
    user = user[0]
    return render_template('edit.html', **user)
    


@app.route('/update', methods=['POST'])
def update():
    # connect to my Database and run insert query
    data = {
        'id': request.form['id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
    }
    mysql = connectToMySQL('CRUD_DB')
    query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s'
    user = mysql.query_db(query, data)
    return redirect('/users')

@app.route('/users/create', methods=['POST'])
def create():
    # validattion check for first Name
    if len(request.form['first_name']) == 0:
        flash('*First Name is required', 'first_name')
    elif not request.form['first_name'].isalpha():
        flash('*Alphabet characters only', 'first_name')

    # validattion check for Last Name
    if len(request.form['last_name']) == 0:
        flash('*Last Name is required', 'last_name')
    elif not request.form['last_name'].isalpha():
        flash('*Alphabet characters only', 'last_name')

    # validattion check for email
    if len(request.form['email']) == 0:
        flash('*Email is required', 'email')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('*Invalid email', 'email')
    else:
        data = {'email': request.form['email'] }
        mysql = connectToMySQL('CRUD_DB')
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result = mysql.query_db(query, data)

        #check if row is greater than zero
        if len(result) > 0:
            flash('*Email already exist', 'email')


    if '_flashes' in session.keys():
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        redirect('/users/new')

    else: # No validation error so insert data to the database
        # get data from the form
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
        }

        # connect to my Database and run insert query
        mysql = connectToMySQL('CRUD_DB')
        query = 'INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s)'
        
        session['new_user_id'] = mysql.query_db(query, data)
        flash("You've been successfully add", 'create')
        return redirect('/users')

if __name__ == '__main__':
    app.run(debug = True)