from flask import Flask, render_template, jsonify, request, flash, session, redirect

from model import connect_to_db

import crud

import os

from jinja2 import StrictUndefined

from datetime import datetime, timezone, timedelta

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
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
    # TODO: only perform second db query if first fails

    # if username exists OR email exists in db and user password matches form password:
    if user_by_username != None and user_by_username.check_password(password):
        # add user to session
        session['user_id'] = user_by_username.user_id
        session['username'] = user_by_username.username
        return jsonify({'status': 'ok', 'username_email': username_email, 'username': user_by_username.username})
    elif user_by_email != None and user_by_email.check_password(password):
        session['user_id'] = user_by_email.user_id
        session['username'] = user_by_email.username
        return jsonify({'status': 'ok', 'username_email': username_email, 'username': user_by_email.username})
    else:
        # display error text 
        return jsonify({'status': 'error', 'msg': 'Sorry, this password and user do not match. Please try again.'})


@app.route('/api/logout')
def logout():
    session.clear()

    return redirect('/')


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
        crud.create_user(username, email, crud.get_hash(create_password))
        return jsonify({'status': 'ok', 'username': username})


@app.route('/add_cellist')
def show_add_cellist_form():
    """Show the add cellist form."""

    return render_template('add_cellist.html', session=session)


@app.route('/add_cellist', methods=["POST"])
def add_cellist():
    """Add a new cellist to the database."""

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
        return jsonify({'status': 'error', 'cellist_id': existing_cellist.cellist_id, 'fname': existing_cellist.fname,
                        'lname': existing_cellist.lname})
    else:
        cellist = crud.create_cellist(fname, lname, cello_details, bio, img_url, music_url)

        return jsonify(
            {'status': 'ok', 'cellist_id': cellist.cellist_id, 'fname': cellist.fname, 'lname': cellist.lname})


@app.route('/api/update_cellist', methods=["POST"])
def update_cellist_from_form():
    """Update an existing cellist in the database."""

    user_id = session['user_id']

    # request.form.get - getting from request, not from html
    cellist_id = request.form.get('cellist_id')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    cello_details = request.form.get('cello_details')
    bio = request.form.get('bio')
    img_url = request.form.get('img_url')
    music_url = request.form.get('music_url')

    if user_id:
        cellist = crud.update_cellist(cellist_id, fname, lname, cello_details, bio, img_url, music_url)
        crud.update_editor(cellist_id, user_id)
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'error'})


@app.route('/all_cellists')
def show_all_cellists():
    """Show all cellists in alphabetical order."""

    all_cellists = crud.get_all_cellists()

    return render_template('all_cellists.html', all_cellists=all_cellists)


@app.route('/api/all_cellists')
def get_all_cellists():
    """Show all cellists in alphabetical order."""

    # TODO: handle the filter query on the back end
    # TODO: pagination on the front end/queries load a few at a time

    all_cellists = crud.get_all_cellists()

    # create py list, loop through cellists
    # add id, fname, lname, img_url, student_links.length, teacher_links.length, posts.length
    # of each cellist to list

    cellist_list = []
    for cellist in all_cellists:
        cellist_list.append(
            {"id": cellist.cellist_id, "name": f"{cellist.fname} {cellist.lname}", "img_url": cellist.img_url,
             "num_teachers": len(cellist.teacher_links), "num_students": len(cellist.student_links),
             "num_posts": len(cellist.posts)})

    return jsonify({'cellist_list': cellist_list})


@app.route('/cellist_profile/<cellist_id>')
def show_cellist(cellist_id):
    """Show a cellist's profile, given cellist id."""

    cellist = crud.get_cellist_by_id(cellist_id)
    posts = crud.get_posts_by_cellist(cellist_id)
    all_cellists = crud.get_all_cellists()
    editor = crud.get_user_by_id(cellist.editor_id)

    return render_template('cellist_profile.html', cellist=cellist, posts=posts, all_cellists=all_cellists,
                           editor=editor)


@app.route('/api/create_link', methods=['POST'])
def create_link_from_profile():
    """Create a link between student and teacher."""

    teacher_id = request.form.get('teacher_id')
    student_id = request.form.get('student_id')
    teacher = crud.get_cellist_by_id(teacher_id)

    # check that id's are not the same
    if teacher_id == student_id:
        return jsonify({'status': 'teacher_eq_student', 'teacher_id': teacher_id, 'student_id': student_id})
    # check whether link already exists in db
    elif crud.check_link(teacher_id, student_id) != None:
        return jsonify({'status': 'link_exists', 'teacher_id': teacher_id, 'student_id': student_id})
    else:
        crud.create_link(teacher_id, student_id)
        return jsonify({'status': 'ok'})


@app.route('/api/add_post', methods=['POST'])
def add_post_from_page():
    """Create a post on a given cellist's profile."""

    # TODO: handle time zones on the front end - JS library?

    user_id = session['user_id']
    cellist_id = request.form.get('cellist_id_from_profile')
    post_content = request.form.get('post_content')
    post_date = datetime.now(timezone.utc)

    new_post = crud.create_post(user_id, cellist_id, post_content, post_date)
    new_username = crud.get_user_by_id(new_post.user_id).username
    new_date = new_post.post_date.strftime('%b. %d, %Y, %H:%M')
    new_content = new_post.content
    new_post_id = new_post.post_id
    new_post_upvotes = new_post.upvotes

    return jsonify({'status': 'ok', 'new_username': new_username, 'new_date': new_date, 'new_content': new_content,
                    'new_post_id': new_post_id, 'new_post_upvotes': new_post_upvotes})


@app.route('/api/upvote_post', methods=['POST'])
def upvote_post_from_post():
    """Add an upvote attached to a given post and user."""

    post_id = request.form.get('post_id')
    user_id = session['user_id']

    # check whether upvote exists
    if crud.get_upvote(user_id, post_id) != None:
        crud.delete_upvote(user_id, post_id)
        msg = "Upvote"
    else:
        crud.create_upvote(user_id, post_id)
        msg = 'Undo Upvote'

    upvotes_count = crud.get_upvotes_count(post_id)

    return jsonify({'status': 'ok', 'upvotes_count': upvotes_count, 'msg': msg})


#########** TREE AND NODE ROUTES **##########

@app.route('/node/<cellist_id>')
def display_oop_tree(cellist_id):
    """Show a cellist node: the cellist and their teachers and students."""

    return render_template('oop_tree.html', cellist_id=cellist_id)


@app.route('/api/node/<cellist_id>')
def get_oop_data(cellist_id):
    """Query the database to create a cellist node, given a cellist id."""

    # query for Cellist object associated with cellist_id
    cellist = crud.get_cellist_by_id(cellist_id)

    # query for links where teacher id is given id
    students_list = crud.get_students_by_cellist_id(cellist_id)
    # query for links where teacher id is given id
    teachers_list = crud.get_teachers_by_cellist_id(cellist_id)

    # create py dict, loop through students, then teachers
    # add id, fname, lname of teacher and each student to dict
    tree_data = {}
    tree_data["id"] = cellist_id
    tree_data["name"] = f"{cellist.fname} {cellist.lname}"
    tree_data["_children"] = []
    tree_data["_parents"] = []
    for student_link in students_list:
        tree_data["_children"].append({"id": student_link.student.cellist_id,
                                       "name": f"{student_link.student.fname} {student_link.student.lname}"})
    for teacher_link in teachers_list:
        tree_data["_parents"].append({"id": teacher_link.teacher.cellist_id,
                                      "name": f"{teacher_link.teacher.fname} {teacher_link.teacher.lname}"})

    # pass through using jsonify to access in D3
    return jsonify({'tree_data': tree_data})


@app.route('/tree/all')  # !! incomplete/in development
def display_mega_tree():
    return render_template('mega_tree.html')


@app.route('/api/tree/all')  # !! incomplete/in development
def get_links_for_tree():
    # add id, fname, lname of teacher to dict
    # add id, fname, lname of each student to dict
    # add each of their students to dict

    # !! add new field in db "has teacher" instead of "Root Node"

    # query for links where teacher id is given id ##!! passing in Root Node for testing
    students_list = crud.get_students_by_cellist_id(49)

    # create py dict, loop through students
    # add id, fname, lname of teacher and each student to dict
    tree_data = {}
    tree_data["id"] = 49
    tree_data["fname"] = "***Root"
    tree_data["lname"] = "Node***"
    tree_data["children"] = []

    def rec_children(cellist_id, tree_data):
        ## ?? cellist_id being the root node?
        ## ?? tree_data being the tree built so far?

        # returns list of student objects [{}, {}, {}]
        students_list = crud.get_students_by_cellist_id(cellist_id)

        # check whether student has students
        # if so, do this same dictionary-building thing with those
        # keep executing for as many levels as exist

        for student_link in students_list:
            tree_data["children"].append({"id": student_link.student.cellist_id, "fname": student_link.student.fname,
                                          "lname": student_link.student.lname,
                                          "children": [rec_children(student_link.student.cellist_id, tree_data)]})
            ## !! need to increment ("progress")
            ##!! queue - enqueue node then its children
            ## !! indicate whether node has been visited
            ## !! tree is a type of graph - similar algorithm
            ## !! what is my base case? - when there are no more children

    return jsonify({'tree_data': tree_data})


if __name__ == '__main__':
    print("we're in server")
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
