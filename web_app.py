from flask import Flask, render_template, request
from forms import LoginForm, CalculatorForm

app = Flask(__name__, static_url_path='/static/css/style.css')
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
    form = CalculatorForm()
    return render_template('calculator.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
    form = LoginForm()
    return render_template('login.html', form=form)
