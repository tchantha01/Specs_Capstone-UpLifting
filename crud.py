# CRUD operations

from model import db, User, Workout, Exercise, Rating, connect_to_db

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

def get_exercises():
    #Show all exercises
    
    return Exercise.query.all()

def get_exercise_by_id( exercise_id):
    #Get an exercise by id
    
    return Exercise.query.get(exercise_id)

def create_rating(user, exercise, score):
    #Create and return a new rating
    
    rating = Rating(user = user, exercise = exercise, score = score)
    
    return rating

def update_rating(rating_id, new_score):
    #Update the rating score
    
    rating = Rating.query.get(rating_id)
    rating.score = new_score
    
if __name__ == "__main__":
    from server import app
    connect_to_db(app)    


    
    