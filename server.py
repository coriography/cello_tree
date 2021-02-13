from flask import Flask, render_template, jsonify, request, flash

from model import connect_to_db

from crud import create_cellist

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_home():

    return render_template('home.html')


@app.route('/', methods=['POST'])
def login():
    """Log in a user, given email or username and password."""
    
    # get username/email and password from AJAX
    username_email = request.form.get('username_email')
    password = request.form.get('login_password')

    # check database if this combo exists
    # if yes, add user to session
    # else, display error text

    flash(f"LOGGED IN {username_email}")
    return "logged in"


# @app.route('/create_account', methods=['POST'])
# def create_account():
#     """Add a new user to the database."""
    
#     # get username/email and password from AJAX
#     # check if username already exists (crud function)
#     username = request.form.get('username')
#     email = request.form.get('email')
#     password = request.form.get('create_password')

#     # add to db (crud function)

#     flash("CREATED ACCOUNT")

#     return redirect("/")
    

@app.route('/add_cellist')
def show_add_cellist_form():

    return render_template('add_cellist.html')


@app.route('/add_cellist', methods=["POST"])
def add_cellist():

    """Add a cellist to the database."""
    # request.form.get - getting from request, not from html
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    cello_details = request.form.get('cello_details')
    bio = request.form.get('bio')
    img_url = request.form.get('img_url')
    music_url = request.form.get('music_url')

    create_cellist(fname, lname, cello_details, bio, img_url, music_url)
    print("created cellist")
    
    return jsonify({'status': 'ok', 'fname': fname, 'lname': lname})





if __name__ == '__main__':
    print("we're in server")
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)