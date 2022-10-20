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
    print('hello')
    data = {
        'user_id': session['user_id']
    }
    # jsonify will serialize data into JSON format.
    return jsonify(Business.get_all_json(data))