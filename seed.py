import os
import model
import server
import crud

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


if __name__ == '__main__':
    print("we're in seed")




