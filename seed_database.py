import os

import model

# os.system('dropdb cello_tree')
# os.system('createdb cello_tree')

model.connect_to_db(server.app)
model.db.create_all()

