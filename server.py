from flask import Flask, render_template, jsonify, request, flash, session

from model import connect_to_db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_home():

    return render_template('home.html')


@app.route('/api/login', methods=['POST'])
def login():
    """Log in a user, given email or username and password."""
    
    # get username/email and password from AJAX
    username_email = request.form.get('username_email')
    password = request.form.get('login_password')

    # get username or email from db
    user_by_username = crud.check_username(username_email)
    user_by_email = crud.check_email(username_email)
    
    # if username exists OR email exists in db and user password matches form password:
    if user_by_username != None and user_by_username.password == password:
        # add user to session
        session['user_id'] = user_by_username.user_id
        return jsonify({'status': 'ok', 'username_email': username_email})
    elif user_by_email != None and user_by_email.password == password:
        session['user_id'] = user_by_email.user_id
        return jsonify({'status': 'ok', 'username_email': username_email})
    else:
        # display error text 
        # TODO: display create account form
        return jsonify({'status': 'error', 'msg': 'NOPE, password does not match a user in the db'})


@app.route('/api/create_account', methods=['POST'])
def create_account():
    """Add a new user to the database."""
    
    # get username/email and password from AJAX
    username = request.form.get('username')
    email = request.form.get('email')
    create_password = request.form.get('create_password')

    # check if username or email already exists (crud function)
    if crud.check_username(username) != None:
        return jsonify({'status': 'username_error', 'username': username})
    elif crud.check_email(email) != None:
        return jsonify({'status': 'email_error', 'email': email})
    else:
        # add to db (crud function)
        crud.create_user(username, email, create_password)
        return jsonify({'status': 'ok', 'username': username})
    

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

    crud.create_cellist(fname, lname, cello_details, bio, img_url, music_url)
    print("created cellist")
    
    return jsonify({'status': 'ok', 'fname': fname, 'lname': lname})
    # TODO: redirect to cellist profile!


@app.route('/cellist_profile/<cellist_id>')
def show_cellist(cellist_id):
    # get cellist from database 
    cellist = crud.get_cellist_by_id(cellist_id)
    # render template and pass in cellist
    return render_template('cellist_profile.html', cellist=cellist)


if __name__ == '__main__':
    print("we're in server")
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)