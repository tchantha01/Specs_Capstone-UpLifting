from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, validators, PasswordField
from wtforms.validators import DataRequired, Length

class WorkoutForm(FlaskForm):
    workout_name = StringField("Workout Name", validators = [DataRequired(), Length(min = 4, max = 225)])
    description = TextAreaField("Description")
    completed = BooleanField("Completed?")
    submit = SubmitField("Submit")

