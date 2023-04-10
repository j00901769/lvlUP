from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import mysql.connector


def connect_to_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="NileSide24",
        database="lvlUP"
        )
    return mydb

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        mydb = connect_to_db()
        cursor = mydb.cursor()
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        values = (email, password)
        cursor.execute(query, values)

        check = cursor.fetchone()
        print(check)
        cursor.close()
        mydb.close()

        if check is None:
            flash('Incorrect Username and/or Password', category='danger')
            return redirect('/login')
        else:
            flash('Success', category='success')
            email = request.form.get('email')
            mydb = connect_to_db()
            cursor = mydb.cursor()
            query = "SELECT name, email, user_type, username FROM users WHERE email = %s"
            value = (email,)
            cursor.execute(query,value)
            user_info = cursor.fetchone()
            print(user_info)
            cursor.close()
            mydb.close()

            session['user'] = user_info
            return redirect('/account')
    return render_template("lvlUP_login.html")

@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect('/login')


# Modify the function to insert the data into the MySQL database
@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_type = request.form.get('user_type')


        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='danger')
        elif len(name) < 2:
            flash('Name must be greater than 1 character', category='danger')
        elif password != confirm_password:
            flash('Passwords do not match', category='danger')
        elif len(password) < 7:
            flash('Password must be at least 7 characters', category='danger')
        elif user_type == None:
            flash('Select your role', category='danger')
        else:
            # Establish a connection to the MySQL database
            mydb = connect_to_db()

            # Create a cursor object to execute SQL statements
            cursor = mydb.cursor()

            # Execute an SQL INSERT statement to insert the data into the appropriate table
            sql = "INSERT INTO users (email, name, username, password, user_type) VALUES (%s, %s, %s, %s, %s)"
            val = (email, name, username, password, user_type)
            cursor.execute(sql, val)

            # Commit the transaction and close the connection
            mydb.commit()
            cursor.close()
            mydb.close()

            flash('Success', category='success')
            return redirect('/login')

    return render_template('lvlUP_signup.html')
