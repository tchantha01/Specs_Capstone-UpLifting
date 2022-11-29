#Server for workout app

from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import db, User, Workout, connect_to_db
from forms import WorkoutForm
import crud


from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "shhhhh"
app.jinja_env.undefined = StrictUndefined

user_id = 1

@app.route('/login')
def login_page():
    #View login page
    
    return render_template("login.html", title = "UP Lifting", page = "login")

@app.route('/')
def homepage():
    #View homepage
    
    workout_form = WorkoutForm()
    
    return render_template("homepage.html", title = "Up Lifting", page = "homepage", workout_form = workout_form)

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
        
    return redirect("/login")
        
        
# @app.route('/user')
# def get_user():
    #View user
    
    # users = crud.get_users()
    
    # return render_template("homepage.html", users = users)    
    
@app.route("/login", methods=["POST"])
def login():
    # Login user
    
    username = request.form.get("username")
    password = request.form.get("password")
    
    
    #Verify is user exist with this username
    user = crud.get_user_by_username(username)    
    
    if not user or user.password != password:
        flash("The username or password you entered is incorrect.")
        
        return redirect("/login")
    else:
        #Log in user by storing the user's username in session
        session["user_username"] = user.username
        flash(f"Welcome back, {user.username}!")
        
    return redirect("/")

@app.route('/logout')
def logout():
    #Logout user
    
    del session["username"]     
    flash("Logged out.")
    
    return redirect('/login')

@app.route('/add_workouts', methods = ["POST"])
def add_workouts():
    #View  created workouts
    
    workout_form = WorkoutForm()
    

    
    if workout_form.validate_on_submit():
        workout_name = workout_form.workout_name.data
        description = workout_form.description.data
        completed = workout_form.completed.data
        
        new_workout = Workout(workout_name, completed, user_id, description = description)
        db.session.add(new_workout)
        db.session.commit()
        
        return redirect(url_for("workout"))
    else:
       return redirect(url_for("workout"))
   
@app.route('/workouts')
def workout():
    #View workout
    
    user = User.query.get(user_id)
    workouts = user.workouts
    
    return render_template("workouts.html", title = "workouts", page = "workout", workouts = workouts, user = user)

@app.route("/update_workout/<workout_id>", methods = ["GET", "POST"])
def update_workout(workout_id):
    #Update a workout
    
    form = WorkoutForm()
    workout = Workout.query.get(workout_id)
    
    if request.method == "POST":
        if form.validate_on_submit():
            workout.workout_name = form.workout_name.data
            if len(form.description.data) > 0:
                workout.description = form.description.data
            workout.completed = form.completed.data
            db.session.add(workout)
            db.session.commit()
            return redirect(url_for("workout"))
        else:
            return redirect(url_for("workout"))
    else:
        return render_template("update_workout.html", title = f"Update {workout.workout_name}", page = "workout", workout = workout, form = form) 
    
@app.route("/delete_workout/<workout_id>")
def delete_workout(workout_id):
    
    workout_to_delete = Workout.query.get(workout_id)
    
    try:
        db.session.delete(workout_to_delete)
        db.session.commit()
        
        flash("Workout was successfully deleted.")
        
        user = User.query.get(user_id)
        workouts = user.workouts
        
        return render_template("workouts.html", title = "Workouts", page = "workout", workouts = workouts)
    
    except:
        # flash("Issues deleting workouts, please try again.")
        
        user = User.query.get(user_id)
        # workouts = user.get_all_workouts()
        workouts = user.workouts
        
        return render_template("workouts.html", title = "Workouts", page = "workout", workouts = workouts)
    
           
    

    

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

@app.route("/exercises/<exercise_id>/ratings", methods = ["POST"])
def create_rating(exercise_id):
    #Rate exercises
    
    logged_in_username = session.get("username")
    rating_score = request.form.get("rating")
    
    if logged_in_username != logged_in_username:
        flash("You must log in to rate an exercise.")
    elif not rating_score:
        flash("ERROR: you did not enter a rating.")   
    else:
        user = crud.get_user_by_username(logged_in_username)
        exercise = crud.get_exercise_by_id(exercise_id)
        rating = crud.create_rating(user, exercise, int(rating_score))
        db.session.add(rating)
        db.session.commit()
        
        flash(f"You rated this exercise {rating_score} out of 5.")     
     
    return redirect(f"/exercises/{exercise_id}")  

@app.route("/update_rating", methods = ["POST"])
def update_rating():
    #Update the rating
    
    rating_id = request.json["rating_id"]
    update_score = request.json["update_score"]
    crud.update_rating(rating_id, update_score)
    db.session.commit()
    
    return "Success!"  


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

