import os
import model
import server
import crud

from test_data import data

os.system('dropdb tree')
os.system('createdb tree')

model.connect_to_db(server.app)
model.db.create_all()


for cellist in data:
    crud.create_cellist(cellist['fname'], cellist['lname'], cellist['cello_details'], cellist['bio'], cellist['img_url'], cellist['music_url'])


if __name__ == '__main__':
    print("we're in seed")




