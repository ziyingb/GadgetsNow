from os import name
import unittest
from app.models import LoginForm
from app import app
import secrets

class TestHello(unittest.TestCase): 
    def test_product_information(self):

    # GIVEN a User model
    # WHEN a new User is created
    # THEN check the username fields are defined correctly
 
        login = LoginForm ('testing@gmail.com', 'testingpassword')
        assert login.usernameoremail == 'testing@gmail.com'
        assert login.password == 'testingpassword'
 
if name == '__main__':
    unittest.main()