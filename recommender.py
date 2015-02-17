# This is the controller file
from flask import Flask, request, render_template, flash, session, jsonify
import json
import model
import os

app = __Flask__(name)

APP_SECRET_KEY = os.environ['APP_SECRET_KEY']


@app.route("/")
def welcome():
	"""The welcome page"""
	return render_template("welcome.html")

@app.route('/signup', methods=['POST'])
def signup():
	user_email = request.form.get('email')
    user_password = request.form.get('password')

    new_user = model.User(email=user_email, password=user_password)

	model.session.add(new_user)
	model.session.commit()

@app.route("/login", methods=["GET"])
def show_login():
    if session.get('user_email'):
        flash("You have successfully logged out.")
        session.clear()
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    users = model.session.query(model.User)
    try:
        user = users.filter(model.User.email==user_email,
                            model.User.password==user_password
                            ).one()
    except InvalidRequestError:
        flash("That email or password was incorrect. " 
            "Please check your login credentials or sign up.")
        return render_template("login.html")

    session['user_email'] = user.email
    session['user_id'] = user.id
    session['count'] = 0
    
    return render_template("welcome.html")


@app.route()
