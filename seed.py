from models import db, User
from app import app

db.drop_all()
db.create_all()

User.query.delete()

u1 = User.register(
    username = "mikeymike",
    password = "12345",
    email = "mikey@gmail.com",
    first_name = "Mikey",
    last_name = "Mike",
)

username = u1.username
password = u1.password
email = u1.email
first_name = u1.first_name
last_name = u1.last_name



db.session.add(u1)
db.session.commit()