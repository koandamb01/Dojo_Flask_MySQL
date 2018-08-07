from flask import Flask, request, redirect, session, render_template, flash
from mysqlconnection import connectToMySQL # import the function connectToMySQL from the file mysqlconnection.py
import re

app = Flask(__name__)
app.secret_key = "medmed"
# create a regular expression object that we can use run operations oncopy
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    mysql = connectToMySQL('emailDB')
    query = "SELECT id, email, DATE_FORMAT(created_at, '%m/%d/%y %r %p') AS created_at FROM users"
    users_list = mysql.query_db(query)
    return render_template('index.html', users=users_list)


@app.route('/adddata', methods=['POST'])
def adddata():
    email = request.form['email']

    if len(email) < 1:
        flash('*Email is required', 'error')

    elif EMAIL_REGEX.match(email):
        # Email is valid then check if email already exist in database
        mysql = connectToMySQL('emailDB')
        query = "SELECT id FROM users WHERE email = %(email)s"
        data = {'email': email}
        data = mysql.query_db(query, data)

        if len(data) < 1:
            # Insert the data here 
            mysql = connectToMySQL('emailDB')
            query = "INSERT INTO users (email) VALUES (%(email)s)"
            data = {'email': email}
            new_user_id = mysql.query_db(query, data)
            flash(f'The email address you entered ({email}) is a VALID email address! Thank you!', 'add')
            print('New row was successfully added to the DB:', new_user_id)
        
        else:
            flash('This email is already taken!', 'error')

    else:
        flash('*Email is invalid', 'error')

    return redirect('/')


@app.route('/delete/<id>')
def delete(id):
    mysql = connectToMySQL('emailDB')
    query = "DELETE FROM users WHERE id = %(id)s"

    data = {
        'id': id
    }
    mysql.query_db(query, data)

    flash('Id delete successfully', 'delete')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug = True)