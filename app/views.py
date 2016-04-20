from flask import render_template, flash, redirect
from app import app
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Denis' } # user's nickname example
    competitions = [ # competitons for loop example in template
    	{
    		'name': 'Competiton 1',
    		'date': '21/04/2016'
    	},
    	{
    		'name': 'Competiton 2',
    		'date': '22/04/2016'
    	}
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        competitions = competitions)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])