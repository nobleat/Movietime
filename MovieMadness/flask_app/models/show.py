from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

db="basic_schema"

class Show:
    def __init__(self, data):
        self.id=data["id"]
        self.title=data["title"]
        self.network=data["network"]
        self.releasedate=data["releasedate"]
        self.description=data["description"]
        self.user_id=data["user_id"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.postedby=None


    @classmethod
    def create(cls,data):
        query="INSERT INTO shows (title, network, releasedate, description, user_id) VALUES (%(title)s, %(network)s, %(releasedate)s, %(description)s, %(user_id)s)"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query= "UPDATE shows SET title = %(title)s, network = %(network)s, releasedate = %(releasedate)s, description = %(description)s WHERE id = %(id)s;"
        results =connectToMySQL(db).query_db(query, data)
        print(results)
        return results

    @classmethod
    def get_one(cls,data):
        query="SELECT * FROM shows JOIN users ON users.id = shows.user_id WHERE shows.id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        thisshow=cls(results[0])
        userinfo={
            "id":results[0]["users.id"],
            "first_name":results[0]["first_name"],
            "last_name":results[0]["last_name"],
            "email":results[0]["email"],
            "password":results[0]["password"],
            "created_at":results[0]["users.created_at"],
            "updated_at":results[0]["users.updated_at"],
        }
        thisshow.postedby=User(userinfo)
        return thisshow

    @classmethod
    def get_all(cls,data):
        query="SELECT * FROM shows"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def destroy(cls,data):
        query="DELETE FROM shows WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)

    # @classmethod
    # def posted_by(cls, data):
    #     query="SELECT * FROM show JOIN users ON users.id = shows.user_id WHERE users.id = %(id)s;"
    #     results= connectToMySQL(db).query_db(query,data)
    #     print(results)
    #     shows=[]
    #     for row in results:
    #         shows.append(cls(row))

    @staticmethod
    def validate_show(show):
        is_valid=True
        if len(show['title']) < 3:
            is_valid=False
            flash("Title must be at least 3 characters","show")
        if len(show['network']) < 3:
            is_valid=False
            flash("Network must be at least 3 characters","show")
        if len(show['description']) < 3:
            is_valid=False
            flash("Description must be at least 3 characters","show")
        if show['releasedate']=="":
            is_valid=False
            flash("Please enter a date","show")
        return is_valid


