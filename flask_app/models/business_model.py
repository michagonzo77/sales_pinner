from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model, class_model
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
        self.lat = data['lat']
        self.lng = data['lng']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls,data):
        query = "INSERT INTO businesses (business_name, first_name, last_name, email, phone, pipeline_status, lat, lng, user_id) VALUES (%(business_name)s, %(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(pipeline_status)s, %(lat)s, %(lng)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE businesses SET business_name = %(business_name)s, year = %(year)s, price = %(price)s, make = %(make)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query="DELETE FROM businesses WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all_json(cls,data):
        query = "SELECT lat, lng FROM businesses WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        return results

    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM businesses WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        all_businesses = []
        for row in results:
            business_data = {
                    **row
                    }
            this_business = cls(row)
            this_business = Business(business_data)
            all_businesses.append(this_business)
        return all_businesses

    @classmethod
    def get_by_id_working(cls,data):
        query = "SELECT * FROM businesses WHERE businesses.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        row = results[0]
        this_business = cls(row)
        return this_business

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