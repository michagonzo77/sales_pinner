from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')         
def landing():
    if "user_id" in session:
        return redirect('/dashboard')
    if "user_id" not in session:
        return render_template("register.html")

@app.route('/users/register', methods=['POST'])
def create_user():
    if not User.validator(request.form):
        return redirect('/')
    hashed = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed
    }
    new_id = User.create(data)
    session['user_id'] = new_id
    return redirect('/dashboard')

@app.route('/users/login/page')         
def user_login():
    if "user_id" in session:
        return redirect('/dashboard')
    if "user_id" not in session:
        return render_template("login.html")

@app.route('/users/login', methods=['POST'])
def login_user():
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Credentials", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Credentials **", "log")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect('/dashboard')

@app.route('/dashboard')
def dash():
    if not "user_id" in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id'],
    }
    logged_user = User.get_by_id(user_data)
    return render_template('dashboard.html', logged_user = logged_user)


@app.route('/users/logout')
def logout():
    del session['user_id']
    return redirect ('/')


@app.route('/favorite/recipe/<int:user_id>/<int:recipe_id>')
def favorite_recipe(user_id,recipe_id):
    data = {
        'user_id': user_id,
        'recipe_id': recipe_id
    }
    User.add_favorite(data)
    return redirect('/dashboard')

@app.route('/favorites/<int:id>')
def get_one(id):
    if not "user_id" in session:
        return redirect('/')
    data = { 'id': id }
    user_data = {
        'id' : session['user_id'],
    }
    logged_user = User.get_by_id(user_data)
    user = User.get_one_with_favorites(data)
    return render_template("favorites.html", user = user, logged_user = logged_user)