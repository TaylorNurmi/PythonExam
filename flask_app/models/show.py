from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import user
bcrypt = Bcrypt(app)


class Show:

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.likes = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL('tvshows').query_db(query)
        shows = []
        for show in results:
            shows.append( cls(show) )
        return shows


    @classmethod
    def get_show_by_title(cls, data):
        query = "SELECT * FROM shows where title = %(title)s;"
        results = connectToMySQL('tvshows').query_db(query, data)
        for row in results:
            return row

    @staticmethod
    def validate_show( data ):
        is_valid = True
        if len(data['title']) < 2: 
            flash("Name not Valid!")
            is_valid = False
        if len(data['network']) < 2: 
            flash("Instructions too short!")
            is_valid = False
        if len(data['description']) < 2: 
            flash("Description too short!")
            is_valid = False
        if data['release_date'] == "mm/dd/yyyy":
            flash("Release datemust be selected")
            is_valid = False
        return is_valid

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO shows ( title, network, release_date, description, user_id ) VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s );"
        return connectToMySQL('tvshows').query_db( query, data )

    @classmethod
    def get_show_by_like(cls, data):
        query = "SELECT * FROM showlikes where show_id = %(id)s;"
        results = connectToMySQL('tvshows').query_db(query, data)
        for row in results:
            return row


    @classmethod
    def get_all_show_likes(cls):
        query = "SELECT * FROM showlikes;"
        results = connectToMySQL('tvshows').query_db(query)
        likes = []
        for row in results:
            likes.append( row )
        return likes


    @classmethod
    def get_show(cls, data):
        query = "SELECT * FROM shows where id = %(id)s;"
        results = connectToMySQL('tvshows').query_db(query, data)
        return results[0]

    @classmethod
    def how_many_liked( cls , data ):
        query = "SELECT * FROM shows LEFT JOIN showlikes ON showlikes.show_id = show.id LEFT JOIN chefs ON showlikes.user_id = users.id WHERE shows.id = %(id)s;"
        results = connectToMySQL('tvshows').query_db( query , data ) 
        shows = cls( results[0] )
        for row in results:
            user_data = {
                "id" : row['id'],
                "first_name": row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['created_at'],
                'updated_at' : row['updated_at']
            }
            shows.likes.append( user.User( user_data ) )
        return shows

    @classmethod
    def likeshow( cls , data ):
        query = "INSERT INTO showlikes (show_id, user_id ) VALUES (%(show_id)s, %(user_id)s);"
        return connectToMySQL('tvshows').query_db( query, data )

    @classmethod
    def deletelike(cls,data):
        query = "DELETE FROM showlikes WHERE show_id = %(show_id)s and user_id = %(user_id)s"
        return connectToMySQL('tvshows').query_db(query, data)

    @classmethod
    def update( cls , data ):
        query = "UPDATE shows SET  title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, user_id = %(user_id)s where shows.id = %(id)s;"
        return connectToMySQL('tvshows').query_db( query, data )

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM shows WHERE shows.id = %(id)s"
        return connectToMySQL('tvshows').query_db(query, data)
