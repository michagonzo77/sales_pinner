from flask_app import app
from flask import render_template, redirect, session, request, flash, jsonify
from flask_app.models.user_model import User
from flask_app.models.business_model import Business

@app.route('/businesses/create', methods=['POST'])
def create_business():
    # If user not logged in, send them home.
    if 'user_id' not in session:
        return redirect('/')
    # If car doesn't pass validation, send them back to form.
    if not Business.validator(request.form):
        return redirect('/dashboard')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    Business.create(data)
    return redirect('/dashboard')

@app.route('/get_businesses')
def get_businesses():
    data = {
        'user_id': session['user_id']
    }
    # jsonify will serialize data into JSON format.
    return jsonify(Business.get_all_json(data))

@app.route('/businesses/<int:id>/edit')
def edit_car(id):
    if 'user_id' not in session:
        return redirect('/')
    this_business = Business.get_by_id_working({'id':id})
    if not this_business.user_id == session['user_id']:
        flash("This aint your prospect!")
        return redirect('/dashboard')
    user_data = {
        'id' : session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    return render_template("business_edit.html", this_business = this_business, logged_user = logged_user)


@app.route('/businesses/<int:id>/update', methods=['POST'])
def update_car(id):
    if not Car.validator(request.form):
        return redirect(f'/cars/{id}/edit')
    car_data = {
        **request.form,
        'id':id
    }
    Car.update(car_data)
    return redirect('/dashboard')