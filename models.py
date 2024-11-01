import datetime
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

# Initialize SQLite database
DATABASE = SqliteDatabase('social.db')

#class for storing users
class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    #stores to database
    class Meta:
        database = DATABASE

    #function to grab all users you follow
    def following(self):
        return (
            User.select().join(
                Relationship, on=Relationship.to_user
            ).where(
                Relationship.from_user == self
            )
        )

    #function to grab all users following you
    def followers(self):

        return (
            User.select().join(
                Relationship, on=Relationship.from_user
            ).where(
                Relationship.to_user == self
            )
        )

    #function to create a user
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=password,
                is_admin=admin
            )
        except IntegrityError:
            raise ValueError("User already exists")
        
#class to store posts
class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    content = TextField()
    user = ForeignKeyField(User)

    #store to database
    class Meta:
        database = DATABASE

#class to store likes
class Like(Model):
    user = ForeignKeyField(User)
    post = ForeignKeyField(Post)

    class Meta:
        database = DATABASE
#class to store comments
class Comment(Model):
    user = ForeignKeyField(User)
    post = ForeignKeyField(Post)
    content = TextField()

    class Meta:
        database = DATABASE
#class defining relationships between users
class Relationship(Model):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')

    class Meta:
        database = DATABASE
        indexes = (
        (('from_user', 'to_user'), True)
        )


        
#initialize database
def initialize():
    DATABASE.connect()
    #creates tables for Users, Posts, Likes, Comments, and Relationships between Users
    DATABASE.create_tables([User, Post, Like, Comment], safe=True)
    DATABASE.close()