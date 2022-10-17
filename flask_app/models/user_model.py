from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[0-9])')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone = data['phone']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, phone, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

# Use to check if email exits in another user while registering and to login user.
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        return False

# Get specific user by their ID, to attach to recipes.
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        return False

    @classmethod
    def add_favorite(cls,data):
        query = "INSERT INTO favorites (user_id, recipe_id) VALUES (%(user_id)s, %(recipe_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_one_with_favorites(cls,data):
        query = "SELECT * FROM users LEFT JOIN favorites ON users.id = favorites.user_id LEFT JOIN recipes ON favorites.recipe_id = recipes.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if results:
            user_instance = cls(results[0])
            recipes_list = []
            for row_from_db in results:
                recipe_data = {
                    'id': row_from_db['recipes.id'],
                    'name': row_from_db['name'],
                    'description': row_from_db['description'],
                    'instructions': row_from_db['instructions'],
                    'date_cooked': row_from_db['date_cooked'],
                    'under_30': row_from_db['under_30'],
                    'created_at': row_from_db['recipes.created_at'],
                    'updated_at': row_from_db['recipes.updated_at'],
                    'user_id': row_from_db['recipes.user_id']
                }
                recipe_instance = recipe_model.Recipe(recipe_data)
                # Creates a variable that uses the User get by ID function to get that users information.
                chef = User.get_by_id(data = {'id':recipe_data['user_id']})
                # Adds a variable to the recipe instance with the user information, for example chef.first_name
                recipe_instance.chef = chef
                # Adds all recipe data plus new variable into list of recipes
                recipes_list.append(recipe_instance)
            # Creates a variable in user instance that includes the list of recipes they favorited 
            user_instance.favorites = recipes_list
            return user_instance
        return results

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