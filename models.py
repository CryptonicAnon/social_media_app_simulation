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
    # #getting posts
    # def get_posts(self):
    #     return Post.select().where(Post.user == self)
    # #getting posts for feed
    # def get_stream(self):
    #     return Post.select().where(
    #         (Post.user << self.following()) |
    #         (Post.user == self)
    #     )
    # #gets users you follow
    # def following(self):
    #     return (
    #         User.select().join(
    #             Relationship, on=Relationship.to_user
    #         ).where(
    #             Relationship.from_user == self
    #         )
    #     )
    # #gets users following you
    # def followers(self):
    #     return (
    #         User.select().join(
    #             Relationship, on=Relationship.from_user
    #         ).where(
    #             Relationship.to_user == self
    #         )
    #     )

    
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

# class Post(Model):
#     timestamp = DateTimeField(default=datetime.datetime.now)
#     user = ForeignKeyField(
#         rel_model=User,
#         related_name='posts'
#     )
#     content = TextField()

#     class Meta:
#         database = DATABASE


# class Relationship(Model):
#     from_user = ForeignKeyField(User, related_name='relationships')
#     to_user = ForeignKeyField(User, related_name='related_to')

#     class Meta:
#         database = DATABASE
#         indexes = (
#             (('from_user', 'to_user'), True)
#         )



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()