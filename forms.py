from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class CalculatorForm(FlaskForm):
    function = SelectField('function', choices=[('1', 'loss sphere'),
                                                ('2', 'loss step'),
                                                ('3', 'loss rastrigin'),
                                                ('4', 'loss rosenbrock')], validators=[DataRequired()])
    param_1 = FloatField('parameter 1', validators=[DataRequired()])
    param_2 = FloatField('parameter 2', validators=[DataRequired()])
    param_3 = FloatField('parameter 3', validators=[DataRequired()])
    param_4 = FloatField('parameter 4', validators=[DataRequired()])
    submit = SubmitField('calculate')
