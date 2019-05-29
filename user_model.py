from sqlite3 import Cursor

from flask import json
from peewee import *
from datetime import datetime

db = SqliteDatabase("F:\\DESKTOP\\db\\blog.db")

class User(Model):
    names = CharField()
    email = CharField(unique=True)
    age = IntegerField()
    password = CharField()
    class Meta:
        database = db


class Product(Model):
    names = CharField()
    quantity = IntegerField()
    price = IntegerField()
    owner = IntegerField()
    date_added = DateField(default=datetime.now())
    class Meta:
        database = db

class Blog(Model):
    author = CharField()
    author_id = CharField()
    title = CharField(unique=True)
    description = CharField()
    date_added = DateField(default=datetime.now())
    class Meta:
        database = db

class Post(Model):
    blog_id = CharField()
    title = CharField(unique=True)
    content = CharField()
    author = CharField()
    date_added = DateField(default=datetime.now())
    class Meta:
        database = db



#User.create_table()
#User.create(names="Kev Robert", email="kev@gmail.com", age=18, password="qwerty")
# person = User.get(User.id == 1)
# print(person.names)
# print(person)

# Product.drop_table()
# Product.create_table()
# Product.create(names="Books", quantity=122, price=70, owner=1 )

# Blog.drop_table()
# Blog.create_table()
# Blog.create(author="Tom Juma", author_id="1", title="First blog title", description="First blog description")
# Blog.create(author="Eric", author_id="2", title="second blog title", description="third blog description")


# blogs = Blog.select()
# blogs_list = []
#
# for blog in blogs:
#     blogs_list.append({"title": blog.title, "description": blog.description, "date_added": blog.date_added})
#
# bl = []
# item1 = [item for item in blogs_list if item['title']=='First blog title']
# bl.append(item1)
# print(bl[0])
# print(blogs_list)

# User.drop_table()
# User.create_table()
# Blog.drop_table()
# Blog.create_table()
# Post.drop_table()
# Post.create_table()
