from wtforms import (
    Form,
    PasswordField,
    validators,
)

class RegistrationForm(Form):
    password = PasswordField(
        'Password',
        [validators.Required(),
        validators.EqualTo(
             'confirm_password',
             message='Passwords does not match'
        )]
    )
    confirm_password  = PasswordField('Repeat Password')