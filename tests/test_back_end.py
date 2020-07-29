import unittest
from flask import url_for
from flask_testing import TestCase
from os import getenv
from Application import app, db, bcrypt
from Application.models import Users, Posts

class TestBase(TestCase):
    
    def create_app(self):
        config_name = "testing"
        app.config.update(SQLALCHEMY_DATABASE_URI=getenv("TEST_DB_URI"),
        SECRET_KEY=getenv("TEST+SECRET_KEY") or "testing",
        WTF_CSRF_ENABLED=False,
        DEBUG=True
        )
        return app

    def setUp(self):
        # this gets called before every test so there's always the same data for the program to test
        db.session.commit()
        db.drop_all()
        db.create_all()
        # this ensures that the databse is completely empty by destroying and rebuilding it
        hashed_pw = bcrypt.generate_password_hash("admin")
        admin = Users(
            first_name="admin", 
            last_name="admin",
            email = "admin@admin.com",
            password = hashed_pw
        )
        # creates the first (admin) test user
        
        hashed_pw_2 = bcrypt.generate_password_hash("password")
        avguser = Users(
            first_name = "test",
            last_name = "user",
            email = "test@user.com",
            password = hashed_pw_2
        )
        # creates the second (non-admin) test user
        db.session.add(admin)
        db.session.add(avguser)
        db.session.commit()
        # this saves the users to the test db, ensuring that every time you run the tests
        # you have the exact same users, ruling user error out of the equation for any bugs that arise

    def tearDown(self):
        # this is called after every test so that the database doesn't get clogged with unneeded data
        # and to reset it to the default values, so one test can't effect another
        db.session.remove()
        db.drop_all()
        # notice that you drop the db here and at the beginning of the setup func,
        # this redundancy ensures that the database will HAVE to be recreated.

class TestViews(TestBase):

    def test_homepage_view(self):
        # this tests to make sure that the homepage is accessible without having to log in
        response = self.client.get(url_for("home"))
        self.assertEqual(response.status_code, 200)
        # if it is, then it should come back with the status code 200, which is what this bit
        # of code is checking, that the status_code is equal to 200
    
class TestPosts(TestBase):
    
    def test_add_new_post(self):
        # tests that you can add a new post and that it redirects you accordingly
        with self.client:
            # you've got to log in here or it won't work!
            self.client.post(
                url_for('login'),
                data = dict(
                    email = "test@user.com",
                    password = "password"
                ),
                follow_redirects = True
            )

            response = self.client.post(
                url_for('post'),
                data = dict(
                    title = "Test Title", 
                    content = "Test Content"
                ),
                follow_redirects = True
            )
            self.assertIn(b"Test Title", response.data)

class TestLogin(TestBase):
    # this will hopefully test the registration form
    def test_login(self):
        with self.client:
            response = self.client.post(
                url_for('login'),
                data = dict(
                    email = "test@user.com",
                    password = "password"
                ),
                follow_redirects = True
            )
            self.assertIn(b"Home", response.data)


class TestRegister(TestBase):
    # this should test the login functionality
    def test_register(self):
        with self.client:
            response = self.client.post(
                url_for('register'),
                data = dict(
                    email = "new@user.com",
                    password = "password",
                    confrim_password = "password",
                    first_name = "Testing",
                    last_name = "Users"
                ),
                follow_redirects = True
            )
            self.assertIn(b"Login", response.data)

class TestLogout(TestBase):
    # this will test out the logout functionality
    def test_logout(self):
        with self.client:
            response = self.client.get(
                '/logout',
                follow_redirects = True
            )
            self.assertIn(b"Login Page", response.data)

class TestUnAuthPost(TestBase):
    # this will test trying to post without being logged in and redirecting you to the login page
    def test_unauthpost(self):
        with self.client:
            response = self.client.get(
                '/newpost',
                follow_redirects = True
            )
            self.assertIn(b"Login Page", response.data)

# class TestAccountDelete(TestBase):
# this should test that when you delete your account it redirects you properly

# class TestEmailInUse(TestBase):
# this will test to see if the correct error message comes up
# if you try to use an email that's already in use

# class TestEditAccountEmailInUse(TestBase):
# this will test to see if the correct error message comes up
# if you try to use an email that's already in use when you edit your account

# class TestEditAccount(TestBase):
# this will test the editing account function

# class TestAuthUserRegister(TestBase):
# this will test a user who's already logged in trying to register

# class TestEmptyPost(TestBase):
# this will test for an empty post

# class TestAuthLogin(TestBase):
# this will test a logged in user trying to log in

# class TestAboutPage(TestBase):
# this will test the about page