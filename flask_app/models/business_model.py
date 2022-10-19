from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model
import re
FORM_REGEX = re.compile(r'^(?=.*?[0-9])')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Business:
    def __init__(self, data):
        self.id = data['id']
        self.business_name = data['business_name']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone = data['phone']
        self.pipeline_status = data['pipeline_status']
        self.user_id = data['user_id']


    @classmethod
    def create(cls,data):
        query = "INSERT INTO businesses (business_name, first_name, last_name, email, phone, pipeline_status, user_id) VALUES (%(business_name)s, %(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(pipeline_status)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE cars SET model = %(model)s, year = %(year)s, price = %(price)s, make = %(make)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query="DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)


    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['business_name']) < 1:
            flash("Business name required.", "business_name")
            is_valid = False
        if len(form_data['first_name']) < 1:
            flash("First name required.", "first_name")
            is_valid = False
        if len(form_data['last_name']) < 1:
            flash("First name required.", "last_name")
            is_valid = False
        if len(form_data['email']) < 1:
            is_valid = False
            flash("Email is required.", "email")
        elif not EMAIL_REGEX.match(form_data['email']): 
            flash("Email is not valid!", "email")
            is_valid = False
        if len(form_data['phone']) < 10:
            flash("Phone required.", "phone")
            is_valid = False
        return is_valid
