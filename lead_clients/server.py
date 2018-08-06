from flask import Flask, request, redirect, session, render_template
from mysqlconnection import connectToMySQL # import the function connectToMySQL from the file mysqlconnection.py

app = Flask(__name__)
app.secret_key = "medmed"

@app.route('/')
def index():
    mysql = connectToMySQL('lead_gen_business')
    query = "SELECT concat_ws(' ', clients.first_name, clients.last_name) AS client_name, COUNT(clients.client_id) AS number_of_leads, ROUND((COUNT(clients.client_id))*100 / (SELECT SUM(number_of_leads) as all_leads FROM(SELECT clients.client_id, concat_ws(' ', clients.first_name, clients.last_name) AS client_name, COUNT(clients.client_id) AS number_of_leads from clients LEFT JOIN sites ON sites.client_id = clients.client_id LEFT JOIN leads ON leads.site_id = sites.site_id GROUP BY clients.client_id) AS results), 2) AS percentage from clients LEFT JOIN sites ON sites.client_id = clients.client_id LEFT JOIN leads ON leads.site_id = sites.site_id GROUP BY clients.client_id" 
    
    clients_leads = mysql.query_db(query)

    # run query to get the total of all
    print(clients_leads)
    return render_template('index.html', clients_leads=clients_leads)

if __name__ == '__main__':
    app.run(debug = True)