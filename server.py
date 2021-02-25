from flask import Flask, render_template, jsonify, request, flash, session

from model import connect_to_db

import crud

from jinja2 import StrictUndefined

from datetime import datetime, timezone, timedelta

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

    # check whether name combo already exists in db
    existing_cellist = crud.get_cellist_by_name(fname, lname)
    if existing_cellist != None:
        return jsonify({'status': 'error', 'cellist_id': existing_cellist.cellist_id, 'fname': existing_cellist.fname, 'lname': existing_cellist.lname})
    else:
        cellist = crud.create_cellist(fname, lname, cello_details, bio, img_url, music_url)

        return jsonify({'status': 'ok', 'cellist_id': cellist.cellist_id, 'fname': cellist.fname, 'lname': cellist.lname})


@app.route('/all_cellists')
def show_all_cellists():
    all_cellists = crud.get_all_cellists()

    return render_template('all_cellists.html', all_cellists=all_cellists)

@app.route('/cellist_profile/<cellist_id>')
def show_cellist(cellist_id):

    cellist = crud.get_cellist_by_id(cellist_id)
    posts = crud.get_posts_by_cellist(cellist_id)
    all_cellists = crud.get_all_cellists()

    return render_template('cellist_profile.html', cellist=cellist, posts=posts, all_cellists=all_cellists)


@app.route('/api/create_link', methods=['POST'])
def create_link_from_profile():

    # TODO: do db query to add teacher using names instead of id's
    # TODO: send teacher/student OBJECT through to be displayed w/ AJAX?

    teacher_id = request.form.get('teacher_id')
    student_id = request.form.get('student_id')

    # check that id's are not the same
    if teacher_id == student_id:
        return jsonify({'status': 'teacher_eq_student', 'teacher_id': teacher_id, 'student_id': student_id})
    # check whether link already exists in db
    elif crud.check_link(teacher_id, student_id) != None:
        return jsonify({'status': 'link_exists', 'teacher_id': teacher_id, 'student_id': student_id})
    else:
        crud.create_link(teacher_id, student_id)
        return jsonify({'status': 'ok', 'teacher_id': teacher_id, 'student_id': student_id})


@app.route('/api/add_post', methods=['POST'])
def add_post_from_page():

    user_id = session['user_id']
    cellist_id = request.form.get('cellist_id_from_profile')
    post_content = request.form.get('post_content')
    post_date = datetime.now(timezone.utc)
    # post_date = "2021-02-14 00:48:25.427639"

    crud.create_post(user_id, cellist_id, post_content, post_date)
    
    return jsonify({'status': 'ok'})
    # TODO: should I append this post to posts??? or wut


@app.route('/api/upvote_post', methods=['POST'])
def upvote_post_from_post():

    post_id = request.form.get('post_id')
    user_id = session['user_id']
    print(user_id)

    crud.create_upvote(user_id, post_id)
    upvotes_count = crud.get_upvotes_count(post_id)

    return jsonify({'status': 'ok', 'upvotes_count': upvotes_count})


@app.route('/tree')
def display_tree_page():

    return render_template('tree.html')


@app.route('/api/mega_tree')
def get_links_for_tree():

    # get all links using db query
    # turn them into nested pydict
    # send back through in a JSON object for D3 display

    # data = {}

    # links = crud.get_all_links
    # for link in links:
    # check whether id exists on any level of dict??
    # !! ^ how??? do I need to order query by whether they have teachers and start with those who don't?
    # add id, fname, lname of teacher to dict
    # add id, fname, lname of each student to dict
    # add each of their students to dict


    # !! add new field in db "has teacher"
    # OR give all same non-teacher by default


    # ?? OR .... if I only display one cellist node at a time
    # !! but.... D3 needs a "root node" and I would have to recalculate every time? idk
    # query a cellist given ID
    # get their teachers
    # get anyone who has listed this cellist as their teacher
    # then when clicking on a new person, query their teachers or students (depending on direction)

    # return jsonify({'data': data})
    pass

@app.route('/api/tree/<cellist_id>')
def show_tree_by_cellist_id(cellist_id):
    # build button in cellist profile with onclick, passes in current cellist_id
    # build ajax file to handle onclick
    # take in cellist id based on button click
    # query for links where teacher id is given id
    students_list = crud.get_students_by_cellist_id(cellist_id)
    # create py dict, loop through students
    # add id, fname, lname of teacher and each student to dict
    tree_data = {}
    tree_data["id"] = cellist_id
    tree_data["fname"] = "fname"
    tree_data["lname"] = "lname"
    tree_data["children"] = []
    for student_link in students_list:
        tree_data["children"].append({"id": student_link.student.cellist_id, "fname": student_link.student.fname, "lname": student_link.student.lname})
    
    # pass through using jsonify
    # access in D3
    # !! use GET request on actual route?
    # return render_template('tree.html')
    return jsonify({'tree_data': tree_data})
    # pass

@app.route('/api/teacher_tree/<cellist_id>')
def show_teacher_tree_by_cellist_id(cellist_id):
    # build button in cellist profile with onclick, passes in current cellist_id
    # build ajax file to handle onclick
    # take in cellist id based on button click
    # query for links where teacher id is given id
    teachers_list = crud.get_teachers_by_cellist_id(cellist_id)
    # create py dict, loop through students
    # add id, fname, lname of teacher and each student to dict
    tree_data = {}
    tree_data["id"] = cellist_id
    tree_data["fname"] = "fname"
    tree_data["lname"] = "lname"
    tree_data["children"] = []
    for teacher_link in teachers_list:
        tree_data["children"].append({"id": teacher_link.teacher.cellist_id, "fname": teacher_link.teacher.fname, "lname": teacher_link.teacher.lname})
    
    # pass through using jsonify
    # access in D3
    # !! use GET request on actual route?
    # return render_template('tree.html')
    return jsonify({'tree_data': tree_data})
    # pass
    


if __name__ == '__main__':
    print("we're in server")
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)