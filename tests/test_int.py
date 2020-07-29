import unittest
import time
from flask import url_for
from urllib.request import urlopen
from os import getenv
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Application import app, db, bcrypt
from Application.models import Users, Posts

# setting the test variables for test admin user
test_admin_first_name =  "admin"
test_admin_last_name = "admin"
test_admin_email = "admin@admin.com"
test_admin_password = "admin"

class TestBase(LiveServerTestCase):
    # this is the class we'll inherit from before every test so that you start with an empty database

    def create_app(self):
        config_name = "testing"
        app.config["SQLALCHEMY_DATABASE_URI"]=getenv("TEST_DB_URI_SECOND")
        app.config["SECRET_KEY"]=getenv("TEST_SECRET_KEY") or "testing"
        return app

    def setUp(self):
        # sets up the test driver and creates some users

        print("<-----NEXT-TEST----->")
        chrome_options = Options()
        chrome_options.binary_location = "L:\CA Learning\chrome-win\chrome.exe"
        chrome_options.add_argument("--headless")
        # this command just means that it will do everything in the background, instead of
        # actually opening a browser and showing you what it's doing
        self.driver = webdriver.Chrome(executable_path="L:\CA Learning\chromedriver.exe", chrome_options=chrome_options)
        self.driver.get("http://localhost:5000")
        db.session.commit()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.driver.quit()
        print("<-----END-OF-TEST----->")

    def test_server_is_up_and_running(self):
        response = urlopen("http://127.0.0.0:5000")
        self.assertEqual(response.code, 200)



class TestRegistration(TestBase):
    def test_registration(self):
        # tests that a user can create an account
        # using the registration form
        # and that if all fields are filled in correctly
        # they'll be redirected to the login page

        self.driver.find_element_by_xpath("/html/body/div[1]/nav/a[5]").click()
        # this navigates to the nav register button in the nav bar
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[1]/input").send_keys(test_admin_email)
        # this inputs the test_admin_email into the email input part of the form
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[2]/input").send_keys(test_admin_password)
        # find the password field
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[3]/input").send_keys(test_admin_password)
        # find the confirm password field, both of these input test_admin_password
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[4]/input").send_keys(test_admin_first_name)
        # find and input the first name field
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[5]/input").send_keys(test_admin_last_name)
        self.driver.find_element_by_xpath("/html/body/div[2]/form/div[6]/input").click()

        assert url_for('login') in self.driver.current_url

        if __name__ == "__main__":
            unittest.main(port=5000)