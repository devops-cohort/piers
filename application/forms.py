from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import users, card_list, deck_list
from application import login_manager, password_hash as pw

class LoginForm(FlaskForm):
    user_name = StringField('User name: ',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )
    password = PasswordField('Password: ',
        validators=[DataRequired(message=None), Length(min=5, max=30)
        ]    
    )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):
    user_name = StringField('User name: ',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )
    first_name = StringField('First name: ',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )
    last_name = StringField('Last name: ',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )
    password = PasswordField('Password: ',
        validators=[DataRequired(message=None), Length(min=5, max=30)
        ]    
    )
    confirm_password = PasswordField('Please confirm your password: ',
        validators=[DataRequired(message=None), Length(min=5, max=30), EqualTo('password')
        ]    
    )
    submit = SubmitField('Register')
    
    def validate_user_name(self, user_name):
        user = users.query.filter_by(user_name=user_name.data).first()
        
        if user:
            raise ValidationError('User name is already in use!')

class CreateCard(FlaskForm):
    card_name = StringField('Card Name: ',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )
    card_attk = IntegerField('Attack: ',
        validators=[DataRequired(message=None)
        ]    
    )
    card_def = IntegerField('Defense: ',
        validators=[DataRequired(message=None)
        ]    
    )
    submit = SubmitField('Create Card')

class CreateDeck(FlaskForm):
    deck_name = StringField('Deck name: ',
    validators=[DataRequired(message=None), Length(min=2, max=30)
        ]    
    )
    submit = SubmitField('Create Deck')

class PasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', 
        validators=[DataRequired()
        ]
    )
    password = PasswordField('Password', 
        validators=[DataRequired()
        ]
    )
    confirm_pass = PasswordField('Password', 
        validators=[DataRequired(), 
            EqualTo('password')
        ]
    )
    submit = SubmitField('Confirm Password')

class AccountForm(FlaskForm):
    user_name = StringField('User Name',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]
    )
    first_name = StringField('First Name',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]
    )
    last_name = StringField('Last Name',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]
    )
    submit = SubmitField('Update Details')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            
            if user:
                raise ValidationError('Email is already in use!')

class EditCardForm(FlaskForm):
    card_name = StringField('User Name',
        validators=[DataRequired(message=None), Length(min=2, max=30)
        ]
    )
    card_attk = IntegerField('Attack: ',
        validators=[DataRequired(message=None)
        ]    
    )
    card_def = card_def = IntegerField('Defense: ',
        validators=[DataRequired(message=None)
        ]    
    )
    submit = SubmitField('Submit Changes')

class SearchCard(FlaskForm):
    card_search = StringField('Search', id='card_autocomplete')
