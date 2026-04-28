from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    post_type = SelectField('Type', choices=[('struggle', 'Struggle Story'), ('advice', 'Advice')], validators=[DataRequired()])
    category = SelectField(
        'Category',
        choices=[
            ('general', 'General'),
            ('CS50', 'CS50'),
            ('CS51', 'CS51'),
            ('CS54', 'CS54'),
            ('CS62', 'CS62'),
            ('CS101', 'CS101'),
            ('CS105', 'CS105'),
            ('CS140', 'CS140'),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField('Submit')

class VideoForm(FlaskForm):
    youtube_url = StringField('YouTube Link', validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField('Preview')