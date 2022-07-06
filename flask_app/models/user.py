import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.shows = []
        self.favorites = []


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (email, first_name, last_name, password) VALUES (%(email)s, %(first_name)s, %(last_name)s, %(password)s);"
        return connectToMySQL("tvshows").query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users where email = %(email)s;"
        results = connectToMySQL("tvshows").query_db(query, data)
        for row in results:
            return row 

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('tvshows').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @staticmethod
    def validate_signup( data ):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if not NAME_REGEX.match(data['first_name']): 
            flash("Invalid First Name!")
            is_valid = False
        if len(data['first_name']) < 2: 
            flash("First Name too short!")
            is_valid = False
        if not NAME_REGEX.match(data['last_name']): 
            flash("Invalid Last Name!")
            is_valid = False
        if len(data['last_name']) < 2: 
            flash("Last Name too short!")
            is_valid = False
        if data['confirm'] != data['password']:
            flash("Passwords DO NOT match")
            is_valid = False
        if len(data['password']) <= 8: 
            flash("Invalid Password!")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_signin( data ):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(data['password']) < 8: 
            flash("Invalid Password!")
            is_valid = False
        return is_valid
    
