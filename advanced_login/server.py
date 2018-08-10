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

@app.route('/')
def home():
    return render_template('home.html', **session)

@app.route('/wall')
def wall():
    if 'user_id' not in session.keys():
        return redirect('/')

    # get user data
    data = {'id': session['user_id']}
    mysql = connectToMySQL('advanced_login_DB')
    query = 'SELECT * FROM users WHERE id = %(id)s'
    users = mysql.query_db(query, data)
    user = users[0]

    if 'user_level' not in session.keys():
        session['user_level'] = user['user_level']

    # check user level
    if user['user_level'] == 9:
        mysql = connectToMySQL('advanced_login_DB')
        users_list = mysql.query_db('SELECT * FROM users')
        return render_template('admin_wall.html', **user, users_list=users_list)
    else:
        return render_template('users_wall.html', **user)

@app.route('/logout')
def logout():
    session.clear() # or session.pop('user_id')
    flash('You have been logged out', 'logout')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    # get the form data
    data = {
        'email': request.form['email'].strip().lower()
    }
    mysql = connectToMySQL('advanced_login_DB')
    query = 'SELECT * FROM users WHERE email = %(email)s'
    row = mysql.query_db(query, data)

    if len(row) > 0:
        user = row[0]
        print('user:', user)
        if bcrypt.check_password_hash(user['password'], request.form['password']):
            session['user_id'] = user['id']
            session['user_level'] = user['user_level']
            return redirect('/wall')
    
    flash('*Email or password invalid', 'login')
    
    return redirect('/')


@app.route('/remove_admin_access/<id>')
def remove_admin_access(id):
    data = {'id': id}
    mysql = connectToMySQL('advanced_login_DB')
    query = 'UPDATE users SET user_level = 1 WHERE id = %(id)s;'
    row = mysql.query_db(query, data)
    return redirect('/wall')


@app.route('/make_admin/<id>')
def make_admin(id):
    data = {'id': id}
    mysql = connectToMySQL('advanced_login_DB')
    query = 'UPDATE users SET user_level = 9 WHERE id = %(id)s;'
    row = mysql.query_db(query, data)
    return redirect('/wall')

@app.route('/remove/<id>')
def remove(id):
    data = {'id': id}
    mysql = connectToMySQL('advanced_login_DB')
    query = 'DELETE FROM users WHERE id = %(id)s;'
    row = mysql.query_db(query, data)
    return redirect('/wall')

######################## @route for Registration #############################
@app.route('/register', methods=['POST'])
def register():
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
        mysql = connectToMySQL('advanced_login_DB')
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result = mysql.query_db(query, data)

        #check if row is greater than zero
        if len(result) > 0:
            flash('*Email already exist', 'email')

    # validation for username
    if len(request.form['username']) == 0:
        flash('*Username is required', 'username')
    else:
        #check if username already exist in the database
        data = {'username': request.form['username'] }
        mysql = connectToMySQL('advanced_login_DB')
        query = 'SELECT * FROM users WHERE username = %(username)s'
        result = mysql.query_db(query, data)

        #check if row is greater than zero
        if len(result) < 1:
            pass # username does not exist
        else:
            flash('*Username already exist', 'username')

    # validation for birthday
    if len(request.form['birthday']) == 0:
        flash('*Birthday is required', 'birthday')
    else:
        this_year = datetime
        mydate = datetime.strptime('2008-01-01', '%Y-%m-%d')
        birth_year = datetime.strptime(request.form['birthday'], '%Y-%m-%d')

        if mydate > birth_year:
            # user is old enough to register
            print('user is old enough to register')
            pass
        else:
            flash('*You are not old enough to register', 'birthday')


    # validaton for gender
    if not request.form.get('gender'):
        flash('*Gender is required', 'gender')
    
    # validattion check for city
    if len(request.form['city']) == 0:
        flash('*City is required', 'city')
    elif not WORD_SPACE_REGEX.match(request.form['city']):
        flash('*Alphabet characters only', 'city')


    # validaton for state
    if len(request.form['state']) == 0:
        flash('*State is required', 'state')

    # validation for zipcode
    if len(request.form['zipcode']) == 0:
        flash('*Zipcode is required', 'zipcode')
    elif not ZIPCODE_REGEX.match(request.form['zipcode']):
        flash('*Invalid zipcode', 'zipcode')

    # validation for password
    if len(request.form['password']) == 0:
        flash('*Password is required', 'password')
    elif len(request.form['password']) < 8:
        flash('*Password must be at least 8 characters', 'password')
    elif not re.search('[0-9]', request.form['password']):
        flash('*Password must have at leat one number', 'password')
    elif not re.search('[A-Z]', request.form['password']):
        flash('*Password must have at least one Caplital letter', 'password')
    elif request.form['password'] != request.form['confirm_password']:
        flash('*Password must be match', 'confirm_password')


    if '_flashes' in session.keys():
        # pass form data to sessions
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        session['username'] = request.form['username']
        session['birthday'] = request.form['birthday']
        session['city'] = request.form['city']
        session['state'] = request.form['state']
        session['zipcode'] = request.form['zipcode']
        return redirect('/')

    else: # No validation error so insert data to the database
        # create an hash password
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        
        # get data from the form
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'username': request.form['username'],
            'birthday': request.form['birthday'],
            'gender': request.form['gender'],
            'city': request.form['city'],
            'state': request.form['state'],
            'zipcode': request.form['zipcode'],
            'password': pw_hash,
            'user_level': 1
        }

        # connect to my Database and run insert query
        mysql = connectToMySQL('advanced_login_DB')
        query = 'INSERT INTO users (first_name, last_name, email, username, birthday, gender, city, state, zipcode, password, user_level) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(username)s, %(birthday)s, %(gender)s, %(city)s, %(state)s, %(zipcode)s, %(password)s, %(user_level)s)'
        
        session['user_id'] = mysql.query_db(query, data)
        flash("You've been successfully registered", 'register')
        return redirect('/wall')




def debug():
    print("*"*20,"Debuging","*"*20)
    print("Form Inputs: ", request.form)
    print("Sessions: ", session)

if __name__ == '__main__':
    app.run(debug = True)