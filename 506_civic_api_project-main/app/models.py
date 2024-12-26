from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

login = LoginManager()
db = SQLAlchemy()

class UserModel(UserMixin, db.Model):
    __tablename__ = 'UserInfo'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(20),nullable=False)
    address = db.Column(db.String(100), nullable=False)
    def __init__(self, email: object, username: object, password: object, address: object) -> object:
        self.email = email
        self.username = username
        self.set_password(password)  # encrypt the password
        self.address = address
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))
