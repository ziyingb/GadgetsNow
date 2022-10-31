from app import sa
from flask_login import UserMixin

class User(sa.Model, UserMixin):
    __tablename__ = "user_tb"
    id = sa.Column(sa.Integer, primary_key = True)
    username = sa.Column(sa.String(120), unique = True, nullable = False)
    email = sa.Column(sa.String(120), unique = True, nullable = False)
    password = sa.Column(sa.String(255), nullable = False)
    salt = sa.Column(sa.String(255), nullable = False)
    verified = sa.Column(sa.Boolean, nullable = False)
    verified_dt = sa.Column(sa.DateTime)

    def __init__(self,username, email, password, salt, verified, verified_dt):
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt
        self.verified = verified
        self.verified_dt = verified_dt

    def __init__(self, username, email, password, salt, verified):
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt
        self.verified = verified

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.username)

    def save(self):
        sa.session.add ( self )
        sa.session.commit( )
        return self 

class UserInformation(sa.Model):
    __tablename__ = "user_info_tb"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user_tb.id"), nullable = True)
    first_name = sa.Column(sa.String(120))
    last_name = sa.Column(sa.String(120))
    mobile_no = sa.Column(sa.Integer, unique= True)
    # Lets users define if this is shipping/billing address later
    address = sa.Column(sa.String(255))
    # Longest Country name is 59
    country = sa.Column(sa.String(60))
    # Longest City name is 187 char ?!
    # "Krung Thep Mahanakhon Amon Rattanakosin Mahinthara Yuthaya Mahadilok Phop Noppharat Ratchathani Burirom Udomratchaniwet Mahasathan Amon Piman Awatan Sathit Sakkathattiya Witsanukam Prasit"
    city = sa.Column(sa.String(200))
    postal_code = sa.Column(sa.Integer)
    last_modified_dt = sa.Column(sa.DateTime)

class ProductInformation(sa.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    name = sa.Column(sa.String(255))
    desc = sa.Column(sa.String(255))
    category = sa.Column(sa.String(120))
    price = sa.Column(sa.Integer)
    url = sa.Column(sa.String(1024))

    def __init__(self, name, desc, category, price, url):
        self.name = name
        self.desc = desc
        self.category = category
        self.price = price
        self.url = url