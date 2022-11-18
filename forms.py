from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

class WorkoutForm(FlaskForm):
    workout_name = StringField("WORKOUT NAME", validators = [DataRequired(), Length(min = 4, max = 225)])
    description = TextAreaField("Description")
    completed = BooleanField("Completed?")
    submit = SubmitField("Submit")
    
    
