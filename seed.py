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


# seed cellist links from cellist_data.py
cellist_id = 0
for cellist in data:
    cellist_id += 1
    # if cellist['teacher_ids'] == [] and cellist['fname'] != "***Root":
    #     crud.create_link(49, cellist_id)
    # else:
    for teacher_id in cellist['teacher_ids']:
        crud.create_link(teacher_id, cellist_id)


# seed user data
for i in range(10):

    username = random.choice([f"cellochick{i}", f"cellobello{i}", f"cellomynameis{i}", f"tinaguofan{i}", f"{i}cellos", f"celloitsme{i}", f"nostrings{i}", f"celloshots{i}"])
    email = f"email{i}@email.com"
    password = f"password{i}"

    crud.create_user(username, email, password)


# seed post data
for cellist in data:
    for i in range(5):
        user_id = random.choice(range(1, 10))
        cellist_id = random.choice(range(1, len(data)))
        content = random.choice(["I met this cellist at the Sitka Cello Festival, 2018! She is a fantastic teacher and taught me how to use bow speed to get a better sound. I hope to work with her again soon!", "Does anyone know where she's teaching this summer? I heard she is releasing a new album soon! Can't wait to hear it.", "Her playing style reminds me of Piatagorsky's - I checked out her Tree and realized that it's because she is 'related' to him! Pretty cool.", "My favorite piece she plays is Salut d'Amour. I learned that piece for my school audition last year.", "We have the same teacher's teacher! Does that make us cello cousins? :)"])
        post_date = datetime.now(timezone.utc) - timedelta(days=i)
        crud.create_post(user_id, cellist_id, content, post_date)



if __name__ == '__main__':
    print("we're in seed")




