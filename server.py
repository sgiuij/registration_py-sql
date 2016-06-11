from flask import Flask, request, render_template, session, redirect, flash
import random
import re
from mysqlconnection import MySQLConnector

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

# our server object!
app = Flask(__name__)
mysql = MySQLConnector(app,'emailregistrationdb')
app.secret_key = "293akljsdf;oaiur7897p987kajsdf;y8"

@app.route('/')
def render_index():    
    return render_template('index.html') 
    
@app.route('/registered')
def create(): 
    query = "SELECT * FROM registered_emails"                          
    registered = mysql.query_db(query)  # run query with query_db()
    return render_template('registered.html',all_reg=registered)

@app.route('/newmail', methods=['POST'])
def display():
    if not EMAIL_REGEX.match(request.form['email']):
        flash('Not a valid email')   
        return redirect('/')
    else:
        query = "INSERT INTO registered_emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {'email': request.form['email']}
        mysql.query_db(query, data)
        return redirect('/registered')

@app.route('/remove_email/<email_id>', methods=['POST'])
def update(email_id):
    query = "DELETE FROM registered_emails WHERE id = :id"
    data = {'id': email_id}
    mysql.query_db(query, data)
    return redirect('/registered')

app.run(debug=True)
