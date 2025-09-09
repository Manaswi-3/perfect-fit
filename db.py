from flask_pymongo import PyMongo

mongo = PyMongo()

def init_app(app):
    global mongo
    mongo.init_app(app)
    return mongo