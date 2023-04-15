from flask import Blueprint, render_template, session, g, redirect, request, flash, url_for
from flask_login import login_required, current_user
import mysql.connector


def connect_to_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="NileSide24",
        database="lvlUP"
        )
    return mydb

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        subject = request.form.get('subject')
        mydb = connect_to_db()
        cursor = mydb.cursor()
        query =  "SELECT u.name, u.email FROM users u\
                    INNER JOIN tutors_subjects ts ON u.user_id = ts.tutor_id\
                    INNER JOIN subjects s ON ts.subject_id = s.subject_id\
                    WHERE s.name = %s AND u.user_type = 'tutor'"
        values = (subject,)
        cursor.execute(query, values)

        tutors = cursor.fetchall()
        print(tutors)
        tutors_data = []
        for tutor in tutors:
            tutor_dict = {'name': tutor[0], 'email': tutor[1]}  # Create a dictionary with name and email fields
            tutors_data.append(tutor_dict)
        cursor.close()
        mydb.close()
        return render_template("lvlUP_home.html", tutors = tutors_data, user=current_user)

    return render_template("lvlUP_home.html", user = current_user)

@views.route('/account', methods = ['GET', 'POST'])
def account():
    if 'user' not in session:
        return redirect('/login')
    mydb = connect_to_db()
    cursor = mydb.cursor()
    query = "SELECT subject_id, name FROM subjects"
    cursor.execute(query)

    subjects = cursor.fetchall()
    print(subjects)
    name, email, user_type, username = session['user']
    return render_template("lvlUP_account.html",
                           name = name, email = email,
                           user_type = user_type,
                           username = username, subjects=subjects)


@views.route('/submit_appointment', methods=['POST'])
def submit_appointment():
    # Retrieve form data from request object
    appointment_id = request.form['appointment_id']
    date = request.form['date']
    duration = request.form['duration']
    student_id = request.form['student_id']
    tutor_id = request.form['tutor_id']
    subject_id = request.form['subject_id']

    # Perform database operations to save form data
    # ... (your code here)

    # Return response or render template
    return "Appointment submitted successfully!"

@views.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@views.route('/about')
def about():
    return render_template("lvlUP_about.html")

@views.route('/contact')
def contact():
    return render_template("lvlUP_contact.html")
