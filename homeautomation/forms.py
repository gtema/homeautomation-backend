# NOT USED
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
# from .models import User


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate(self):
        if not Form.validate(self):
            print(self.errors)
            return False
        return True


class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])
