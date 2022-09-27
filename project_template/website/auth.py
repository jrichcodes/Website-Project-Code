from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", text ="testing")

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/new-trip', methods=['GET', 'POST'])
def new_trip():
    if request.method == 'POST':
        return redirect(url_for('views.home')) #redirect to home page after new account created
    return render_template("new_trip.html")


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #add user to database
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='sucess')
            return redirect(url_for('views.events')) # redirect to events page after new account created


    return render_template("sign_up.html")