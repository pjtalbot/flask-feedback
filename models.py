from enum import unique
from multiprocessing import AuthenticationError
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

class User(db.Model):
    """Model for users"""

    __tablename__= 'users'
   

   
    username = db.Column(db.String(), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.Text(), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hashed_pw = bcrypt.generate_password_hash(password)
        hashed_pw_utf8 = hashed_pw.decode("utf8")
        user = cls(username=username, 
                    password=hashed_pw_utf8,
                    email=email, 
                    first_name=first_name, 
                    last_name=last_name
                    )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    # def to_dict(self):
    #     """Serialize cupcake to dict"""

    #     return {
    #         "id": self.id,
    #         "flavor": self.flavor,
    #         "rating": self.rating,
    #         "size": self.size,
    #         "image": self.image,
    #     }
        

def connect_db(app):
    db.app = app
    db.init_app(app)