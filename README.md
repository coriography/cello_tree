# Cello Tree :notes: :deciduous_tree:

Cello Tree is a “family tree” of cellists, joined by teacher-student links, revealing connections among the international cellist community across generations. Users can browse Cello Tree for their favorite cellists, or create an account to add and update new cellists - along with their teachers and students - to the database. Users can upload a photo, include a link to the artist’s music, write about the instrument they perform on, and share stories about other cellists in a forum (and upvote their favorite posts). Whether you’ve played cello for one year or fifty years, you perform on YouTube or in Carnegie Hall, or you just want to explore the lives and music of cellists, you can contribute, share stories, and help grow the Cello Tree.

**Front end:** JavaScript/jQuery, AJAX, JSON, HTML/Jinja, CSS/Bootstrap, D3.js (data visualization library)
**Back end:** Python/Flask, SQL/PostgreSQL, SQLAlchemy ORM, Cloudinary API (media hosting)

View technical demo on YouTube: https://www.youtube.com/watch?v=RK0CSYA__Ec


![app screenshot](/static/img/home.png)
![app screenshot](/static/img/all_cellists.png)
![app screenshot](/static/img/add_cellist.png)
![app screenshot](/static/img/profile.png)
![app screenshot](/static/img/tree.png)
![app screenshot](/static/img/forum.png)


## Usage :desktop_computer:

Requirements:
Python3
PostgreSQL

To run locally:

1. Clone this repository to your machine:

```
$ git clone https://github.com/coriography/cello_tree
```

2. Create virtual environment:

```
$ python3 -m venv env
```

3. Activate your virtual environment:

```
$ source env/bin/activate
```

4. Install dependencies:

```
$ pip3 install -r requirements.txt
```

5. Set a secret key to run Flask by creating /secrets.sh in your root directory:

![app screenshot](/static/img/secret_key.png)

6. Add your key to your environmental variables:

```
$ source secrets.sh
```
```

7. Create database and populate the app with data:

```
$ python3 seed.py
```

8. Launch the server:

```
$ python3 server.py
```

9. Go to localhost:5000 in your browser


## Roadmap :blue_car:

Up next:

1. add the YouTube and Spotify API’s to make it easier to link a cellist with their music
2. add a “verified” feature so that a cellist can have ownership and exclusive edit access to their own profile
3. implement the security features needed to deploy the app


## About this project :woman_technologist:

Built by [Cori Lint](https://github.com/coriography), with many thanks to [justincy](https://github.com/justincy/d3-pedigree-examples) for his example of a D3.js "Tree" with both ancestors and descendants.

Cori is cellist-turned-software engineer with a knack for motivating and inspiring others. As her career has evolved from performance, to production, to web design, to software engineering, she has continued to seek growth and creative solutions. Cori brings to the tech industry leadership abilities, persistence, focus, empathy, and good judgment, along with a strong set of technical skills and prior experience in web development. She is a Summa Cum Laude graduate of the University of Michigan, and an active member of Artists Who Code, an online community that advocates for creative professionals in the tech industry.

Contact Cori on [LinkedIn](https://www.linkedin.com/in/cori-lint/)