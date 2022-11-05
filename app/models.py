from datetime import datetime
from app import sa
from flask_login import UserMixin

class User(sa.Model, UserMixin):
    __tablename__ = "user_tb"
    id = sa.Column(sa.Integer, primary_key = True, nullable= False, unique = True)
    username = sa.Column(sa.String(120), unique = True, nullable = False)
    email = sa.Column(sa.String(120), unique = True, nullable = False)
    password = sa.Column(sa.String(255), nullable = False)
    salt = sa.Column(sa.String(255), nullable = False)
    is_active= sa.Column(sa.Integer, default=0)
    verified_dt = sa.Column(sa.DateTime, nullable = True)

    def __init__(self, id, username, email, password, salt, is_active, verified_dt):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt
        self.is_active = is_active
        self.verified_dt = verified_dt

    def __init__(self, id, username, email, password, salt):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt

    def set_verified(self):
        self.is_active= 1
        self.verified_dt = datetime.now()
        sa.session.commit()
        return self 

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.username)

    def save(self):
        sa.session.add (self)
        sa.session.commit()
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

    def __init__(self, user_id, first_name, last_name, mobile_no, address, country, city, postal_code, last_modified_dt):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.mobile_no = mobile_no
        self.address = address
        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.last_modified_dt = last_modified_dt
        

    def __init__(self, user_id, last_modified_dt):
        self.user_id = user_id
        self.last_modified_dt = last_modified_dt
    
    
    def update_information(self, first_name, last_name, mobile_no, address, country, city, postal_code, last_modified_dt):
        self.first_name= first_name
        self.last_name = last_name
        self.mobile_no = mobile_no
        self.address = address
        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.last_modified_dt = last_modified_dt
        sa.session.commit()
        return self 


    def save(self):
        sa.session.add (self)
        sa.session.commit()
        return self 

class ProductInformation(sa.Model):
    id = sa.Column(sa.Integer, primary_key = True)
    name = sa.Column(sa.String(255))
    desc = sa.Column(sa.String(255))
    category = sa.Column(sa.String(120))
    price = sa.Column(sa.Integer)
    url = sa.Column(sa.String(1024))
    price_stripe = sa.Column(sa.String(255))

    def __init__(self, name, desc, category, price, url, price_stripe):
        self.name = name
        self.desc = desc
        self.category = category
        self.price = price
        self.url = url
        self.price_stripe = price_stripe

    def save(self):
        sa.session.add ( self )
        sa.session.commit()
        return True 

    def add(self):
        sa.session.add(self)
        sa.session.commit()
        return True