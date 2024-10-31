import datetime
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

# Initialize SQLite database
DATABASE = SqliteDatabase('social.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password).decode('utf8'),
                is_admin=admin
            )
        except IntegrityError:
            raise ValueError("User already exists")
        
class Relationship(Model):
    from_user = ForeignKeyField(User, backref='relationships')
    to_user = ForeignKeyField(User, backref='related_to')

    class Meta:
        indexes = (
            (('from_user', 'to_user'), True),
        )

class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    content = TextField()
    user = ForeignKeyField(User)

    class Meta:
        database = DATABASE
        
        

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()