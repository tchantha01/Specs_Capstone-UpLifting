#Server for workout app

from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import db, User, Workout, Exercise, connect_to_db
from forms import WorkoutForm
import crud


from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "shhhhh"
app.jinja_env.undefined = StrictUndefined

user_id = 1

@app.route('/')
def homepage():
    #View homepage
    
    return render_template("homepage.html", title = "Up Lifting", page = "homepage")

@app.route('/users', methods=["POST"])
def register_user():
    #Create a new user
    
    username = request.form.get("username")
    password = request.form.get("password")
    
    user = crud.get_user_by_username(username)
    
    if user:
        flash("Cannot create an account with that username. Please try again.")
    else:
        user = crud.create_user(username, password)
        db.session.add(user)
        db.session.commit()
        flash("New account created! Please log in.")
        
        return redirect('/')
    
@app.route('/user')
def get_user():
    #View user
    
    users = crud.get_users()
    
    return render_template("homepage.html", users = users)    
    
@app.route('/login', methods=["POST"])
def login():
    # Log in user
    
    username = request.form.get("username")
    password = request.form.get("password")
    
    #Verify is user exist with this username
    user = crud.get_user_by_username(username)    
    
    if not user or user.password != password:
        flash("The username or password you entered is incorrect.")
    else:
        #Log in user by storing the user's username in session
        session["user_username"] = user.username
        flash(f"Welcome back, {user.username}!")
        
    return render_template("workouts.html", title = "workouts", page = "workouts", username = user.username, password = user.password, user = user)      

@app.route('/logout')
def logout():
    #Logout user
    
    del session["username"]     
    flash("Logged out.")
    
    return redirect('/')

@app.route('/workouts')
def workouts(self):
    #View workouts
    
    workout_form = WorkoutForm()
    
    user = crud.get_user_by_id(user_id)
    workouts = User.get_all_workouts(self)
    
    
    
    return render_template("workouts.html", title = "workouts", page = "workouts", workout_form = workout_form, workouts = workouts, user = user)

@app.route('/add_workout', methods = ["POST"])
def add_workout():
    #Create a new workout
    
    workout_form = WorkoutForm()
    
    if workout_form.validate_on_submit():
        workout_name = workout_form.workout_name.data
        description = workout_form.description.data
        completed = workout_form.completed.data
        
        new_workout = Workout(workout_name, description = description, completed = completed)
        db.session.add(new_workout)
        db.session.commit()
        
        return redirect(url_for("workouts"))
    else:
        return redirect(url_for("workouts"))
    

@app.route('/exercises')
def get_exercises():
    #Show the list of exercises
    
    exercises = crud.get_exercises()

    return render_template("exercises.html", title = "exercises", page = "exercises", exercises = exercises)

@app.route('/exercises/<exercise_id>')
def show_exercises(exercise_id):
    #Show description of each exercise
    
    exercise = crud.get_exercise_by_id(exercise_id)
    
    return render_template("exercise_detail.html", page = "exercises", exercise = exercise)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

