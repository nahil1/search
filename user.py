from werkzeug.security import generate_password_hash, check_password_hash
from config import get_settings, set_settings
from flask_login import UserMixin


class User(UserMixin):
    id = 'Admin'

    def set_password(self, password):
        set_settings(password=generate_password_hash(password))
    
    def check_pasword(self, password):
        return check_password_hash(get_settings('password'),  password)
