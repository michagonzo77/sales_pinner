from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import business_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[0-9])')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

# Use to check if email exits in another user while registering and to login user.
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        return False

# Get specific user by their ID, to attach to businesses.
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        return False

# Validate user creating account.
    @staticmethod
    def validator(potential_user):
        print(potential_user)
        is_valid = True
        if len(potential_user['first_name']) < 2:
            is_valid = False
            flash("First name is required.", "first_name")
        if len(potential_user['last_name']) < 2:
            is_valid = False
            flash("Last name is required.", "last_name")
        if len(potential_user['email']) < 1:
            is_valid = False
            flash("Email is required.", "email")
        elif not EMAIL_REGEX.match(potential_user['email']): 
            flash("Email is not valid!", "email")
            is_valid = False
        else:
            user_in_db = User.get_by_email({'email':potential_user['email']})
            if user_in_db:
                flash("Email already registered!", "email")
                is_valid = False
        if len(potential_user['password']) < 8:
            is_valid = False
            flash("Password must be 8 characters.", "password")
        # Password must contain 1 capital letter and 1 number.
        elif not PASSWORD_REGEX.match(potential_user['password']):
            flash("At least 1 uppercase and 1 number required with a total of 8 characters.", "password")
            is_valid = False
        elif potential_user['password'] != potential_user['confirm_pass']:
            flash("Double check your password confirmation.", "password2")
            is_valid = False
        return is_valid