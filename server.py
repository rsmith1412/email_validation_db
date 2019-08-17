from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "the most secret"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/validate', methods=["POST"])
def validate():
    print("Got post info")
    print(request.form)
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address!")
        return redirect("/")
    mysql = connectToMySQL('email_validation_db')
    query = "INSERT INTO email (email) VALUES (%(em)s);"
    data = {
        "em": request.form["email"]
    }
    session["id"] = mysql.query_db(query, data)
    session["email"] = request.form["email"]
    print(session["email"])
    return redirect("/success")

@app.route('/success')
def display_email():
    print("Got session id")
    print(session["id"])
    mysql = connectToMySQL('email_validation_db')
    query = "SELECT * FROM email;"
    data = {
        "id": session["id"]
    }
    display_emails = mysql.query_db(query, data)
    last_email = session["email"]
    # print(last_index)
    if session["id"] != None:
        flash(f" The email address you entered {last_email} is a VALID email address! Thank you!")
    else:
        flash("Email successfully deleted!")
    print("////", display_emails)
    return render_template("success.html", emails = display_emails)

@app.route('/<id>/destroy')
def destroy_email(id):
    print("Let's destroy this id")
    print(id)
    mysql = connectToMySQL('email_validation_db')
    query = "DELETE FROM email WHERE id = %(id)s;"
    data = {
        "id": id
    }
    session["id"] = mysql.query_db(query, data)
    print("////", session["id"])
    return redirect('/success')

if __name__ == "__main__":
    app.run(debug=True)