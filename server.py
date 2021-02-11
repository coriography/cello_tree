from flask import Flask, render_template

from model import connect_to_db

from crud import create_cellist

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_home():

    return render_template('home.html')

@app.route('/add_cellist')
def add_cellist():

    return render_template('add_cellist.html')

@app.route('/data/<int:cellist_id')
def add_cellist():
    """Add a cellist to the database."""

    # create_cellist(fname, lname, location, cello_details, bio, img_url, music_url)
    
    return "this is the return from server"


if __name__ == '__main__':
    print("we're in server")
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)