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
    
    return User.query.filter_by(username = username).first()

# def get_all_workouts(self):
    #Get all workouts
    
    # workouts = []
    
    # for user in self.username:
    #     for workout in user.workouts:
    #         workouts.append(workout)
            
    # return workouts        
    

def create_exercise(exercise_name, description, exercise_img):
    
    exercise = Exercise(exercise_name = exercise_name, description = description, exercise_img = exercise_img)
    
    return exercise

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


    
    