from flask import render_template
from app import app

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
