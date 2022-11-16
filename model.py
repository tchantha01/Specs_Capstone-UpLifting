#Models for viewing workout app
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#Create classes

class User(db.Model):
    
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    
    workouts = db.relationship("Workout", backref = "user", lazy = True) 
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def get_all_workouts(self):
        workouts = []
        
        for user in self.users:
            for workout in user.workouts:
                workouts.append(workout) 
                
        return workouts           
        
class Workout(db.Model):
    
    __tablename__ = 'workouts'
    
    workout_id =db.Column(db.Integer, primary_key = True, autoincrement = True)
    workout_name = db.Column(db.String(225), nullable = False)
    description = db.Column(db.String(255), nullable = True)
    completed = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    
    def __init__(self, workout_name, completed, user_id, **kwargs):
        self.workout_name = workout_name
        self.completed = completed
        self.user_id = user_id
        
        if "description" in kwargs:
            self.description = kwargs["description"]
            
class Exercise(db.Model):
    
    __tablename__ = 'exercises'
    
    exercise_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    exercise_name = db.Column(db.String(225))
    description = db.Column(db.Text)
    exercise_img = db.Column(db.String(225))   
    
    def __repr__(self):
        return f"<Exercise exercise_id = {self.exercise_id} title = {self.title}>"
    
class Rating(db.Model):
    
    __tablename__ = 'ratings'
    
    rating_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    score = db.Column(db.Integer)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.exercise_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    
    exercise = db.relationship("Exercise", backref = "ratings")
    user = db.relationship("User", backref = "ratings")
    
    def __repr__(self):
        return f"<Rating rating_id = {self.rating_id} score = {self.score}>"
    
def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo = True):
        flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        flask_app.config["SQLALCHEMY_ECHO"] = echo
        flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        
        db.app = flask_app
        db.init_app(flask_app)
        
        print("Connected to database!")
        
if __name__ == "__main__":
    from server import app
    connect_to_db(app, echo = False)          
                
    
    
    
    
    
    
           