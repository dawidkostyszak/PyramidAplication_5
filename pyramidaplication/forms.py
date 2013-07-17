from formencode import (
    FancyValidator,
    Invalid,
    Schema,
    validators,
)

from .models import (
    DBSession,
    User,
)


class CheckLogin(FancyValidator):

    min = 4
    max = 15
    messages = {
        'to_short': 'Your login must be longer than %(min)i characters.',
        'to_long': 'Your login must be shorter than %(max)i characters.',
        'no_login': 'Please add login.',
        'error': 'You can not use space in login.',
        'exists': 'That username already exists please try another.',
    }

    def _to_python(self, value, state):
        if len(value) < self.min:
            raise Invalid(
                self.message(
                    "to_short",
                    state,
                    min=self.min
                ),
                value,
                state
            )

        if len(value) > self.max:
            raise Invalid(
                self.message(
                    "to_long",
                    state,
                    min=self.max
                ),
                value,
                state
            )

        if len(value) == 0:
            raise Invalid(
                self.message(
                    "no_login",
                    state
                ),
                value,
                state
            )

        if DBSession.query(User).filter_by(login=value).first():
            raise Invalid(
                self.message(
                    "exists",
                    state
                ),
                value,
                state
            )

        return value


class CheckPassword(FancyValidator):

    min = 8
    max = 30
    messages = {
        'to_short': 'Your password must be longer than %(min)i characters.',
        'to_long': 'Your password must be shorter than %(max)i characters.',
        'no_password': 'Please add password.',
        'error': 'You can not use space in password.'
    }

    def _to_python(self, value, state):
        if len(value) < self.min:
            raise Invalid(
                self.message(
                    "to_short",
                    state,
                    min=self.min
                ),
                value,
                state
            )

        if len(value) > self.max:
            raise Invalid(
                self.message(
                    "to_long",
                    state,
                    min=self.max
                ),
                value,
                state
            )

        if len(value) == 0:
            raise Invalid(
                self.message(
                    "no_password",
                    state
                ),
                value,
                state
            )

        return value


class RegistrationForm(Schema):

    allow_extra_fields = True
    filter_extra_fields = True

    login = CheckLogin()
    password = CheckPassword()
    confirm_password = validators.String()
    chained_validators = [
        validators.FieldsMatch(
            'password',
            'confirm_password',
            messages=dict(invalidNoMatch='Password does not match'),
        )
    ]


class ValidateLogin(FancyValidator):

    def _to_python(self, value, state):
        if not value:
            raise Invalid(
                'Please add login.',
                value,
                state
            )
        return value


class ValidatePassword(FancyValidator):

    def _to_python(self, value, state):
        if not value:
            raise Invalid(
                'Please add password.',
                value,
                state
            )

        if not DBSession.query(User).filter_by(
                login=state.full_dict['login'],
                password=value
        ).first():
            raise Invalid(
                'Wrong login or password.',
                value,
                state
            )
        return value


class LoginForm(Schema):

    allow_extra_fields = True
    filter_extra_fields = True

    login = ValidateLogin()
    password = ValidatePassword()
