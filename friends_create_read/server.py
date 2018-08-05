from flask import Flask, render_template, request, redirect, session
from mysqlconnection import connectToMySQL # import the function connectToMySQL from the file mysqlconnection.py

app = Flask(__name__)
app.secret_key = "monkey"
# images = Images(app)


@app.route('/')
def index():
    mysql = connectToMySQL('myfriendsdb')
    friends = mysql = mysql.query_db('SELECT * FROM friends')
    return render_template('index.html', friends = friends)

@app.route('/connect', methods=['POST'])
def connect():
    mysql = connectToMySQL('myfriendsdb')
    query = 'INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(firstname)s, %(lastname)s, %(occupation)s, NOW(), NOW());'
    
    data = {
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'occupation': request.form['occupation']
    }
    new_friend_id = mysql.query_db(query, data)
    return redirect('/')

# Run server
if __name__ == '__main__':
    app.run(debug = True)