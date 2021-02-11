from flask import Flask, render_template

from model import connect_to_db

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_home():
    return render_template('home.html')


if __name__ == '__main__':
    print("we're in server")
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)