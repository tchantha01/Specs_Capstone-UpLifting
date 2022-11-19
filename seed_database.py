#Script to seed database

#Import statements
import os
import json



import crud
import model
import server

#Script to re-create database
os.system("dropdb uplifting")
os.system("createdb uplifting")

#Connect to the database and call db.create_all()
model.connect_to_db(server.app, echo = False)
model.db.create_all()

#Load data from json file and set to variable
with open("data/exercises.json") as f:
    exercise_data = json.loads(f.read())
    
#Create exercises, store them in list so we can use them to create ratings     
exercises_in_db = []
for exercise in exercise_data:
    exercise_name, description, exercise_img = (
        exercise["exercise_name"],
        exercise["description"],
        exercise["exercise_img"],
    )
    
    db_exercise = crud.create_exercise(exercise_name, description, exercise_img) 
    exercises_in_db.append(db_exercise)

model.db.session.add_all(exercises_in_db)
model.db.session.commit()  