# CRUD operations

from model import db, User, Workout, Rating, connect_to_db

def create_user(username, password):
    #Create a new user
    
    user = User(username = username, password = password)
    
    return user

def get_users():
    #Get all users
    
    return User.query.all()

def get_user_by_id(user_id):
    #Get user by id
    
    return User.query.get(user_id)

def get_user_by_username(username):
    #Get user by username
    
    return User.query.filter(User.username == username).first()


    