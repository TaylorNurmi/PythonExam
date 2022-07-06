from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/shows')
def dashboard():
    if 'user_id' in session:
        data = {
            "id": session["user_id"]
        }
        shows = Show.get_all()
        likes = Show.get_all_show_likes()
        checker = len(likes)
        return render_template("allshows.html", shows = shows, likes = likes, checker = checker)
    else:
        return redirect('/')

@app.route('/signup', methods = ['Post'])
def signup():
    data = { 
        "email" : request.form["email"] 
        }
    user_exists = User.get_user_by_email(data)
    if user_exists:
        flash("email already in use")
        return redirect("/")
    if not User.validate_signup(request.form):
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "email": request.form["email"],
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "password": pw_hash,
            "confirm": request.form["confirm"]
        }
        user_id = User.save(data)
        session['user_id'] = user_id
        session['user_name'] = request.form["first_name"]
    return redirect("/shows")

@app.route('/login', methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"] 
        }
    user_exists = User.get_user_by_email(data)
    if not user_exists:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_exists['password'], request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_exists['id']
    session['user_name'] = user_exists['first_name']
    return redirect("/shows")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')