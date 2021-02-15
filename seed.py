import os
import model
import server
import crud
import random

from datetime import datetime, timezone, timedelta

from cellist_data import data

os.system('dropdb tree')
os.system('createdb tree')

model.connect_to_db(server.app)
model.db.create_all()

# seed cellist data from cellist_data.py
for cellist in data:
    crud.create_cellist(cellist['fname'], cellist['lname'], cellist['cello_details'], cellist['bio'], cellist['img_url'], cellist['music_url'])


# seed user data
for i in range(10):

    username = f"username{i}"
    email = f"email{i}@email.com"
    password = f"password{i}"

    crud.create_user(username, email, password)


# seed post data
for cellist in data:
    for i in range(5):
        user_id = random.choice(range(1, 10))
        cellist_id = random.choice(range(1, len(data)))
        content = f"{i} Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        post_date = datetime.now(timezone.utc) - timedelta(days=i)
        crud.create_post(user_id, cellist_id, content, post_date)



if __name__ == '__main__':
    print("we're in seed")




