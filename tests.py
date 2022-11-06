from os import name
import unittest 
import flask 
from app import app 
import secrets 

class TestHello(unittest.TestCase): 
    def setUp(self): 
        app.testing = True 
        self.app = app.test_client() 
        app.secret_key = secrets.token_urlsafe(16) 
 
    def test_landing(self): 
        rv = self.app.get('/') 
        self.assertEqual(rv.status, '200 OK') 
 
    def test_register(self): 
        # user register 
        rv = self.app.post('/register', data={ 
            "username": "test",
            "email": "test@test.com" ,
            "password": "test"
        }) 
        assert('{"status": "Register successful"}' in rv.data.decode("utf-8")) 

    def test_register_username_taken(self): 
        # user register username taken 
        rv = self.app.post('/register', data={ 
            "username": "test",
            "email": "test@test.com", 
            "password": "test"
        }) 
        rv = self.app.post('/register', data={ 
            "username": "test",
            "email": "test@test.com",
            "password": "test"
        }) 
        assert('{"status": "Username taken"}' in rv.data.decode("utf-8"))

        # user account logout 
        rv = self.app.get('/logout', follow_redirects=True) 
        assert('<input class="login-input input' in rv.data.decode("utf-8"))\
        
        # home page 
        rv = self.app.get('/', follow_redirects=True) 
        assert('<td>10</td>\n' in rv.data.decode("utf-8")) 

if name == '__main__': 
    unittest.main()