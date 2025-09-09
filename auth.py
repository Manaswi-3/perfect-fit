from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import mongo

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    users = mongo.db.users

    if request.method == "POST":
        action = request.form.get("action")

        if action == "signup":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            if password != confirm_password:
                flash("Passwords do not match!")
                return redirect(url_for("auth.login"))

            if users.find_one({"username": username}):
                flash("Username already exists. Try another.")
                return redirect(url_for("auth.login"))

            hashed_pw = generate_password_hash(password)

            users.insert_one({
                "username": username,
                "email": email,
                "password": hashed_pw,
                "role": "user"     
            })

            session["username"] = username
            session["role"] = "user"
            flash("Signup successful! Welcome.")
            return redirect(url_for("guide"))

        elif action == "signin":
            username = request.form.get("username")
            password = request.form.get("password")
            user = users.find_one({"username": username})

            if user and check_password_hash(user["password"], password):
                session["username"] = username
                session["role"] = user.get("role", "user")  
                flash("Login successful!")

                if session["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))
                else:
                    return redirect(url_for("guide"))
            else:
                flash("Invalid login credentials")
                return redirect(url_for("auth.login"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("role", None)  
    flash("You have been logged out")
    return redirect(url_for("index"))
