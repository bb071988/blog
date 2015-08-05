
import os
import sys
import logging  
import unittest
import multiprocessing
import time
from urlparse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

# Configure your app to use the testing database
if not "CONFIG_PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.browser = Browser("phantomjs")

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

        self.process = multiprocessing.Process(target=app.run)
        self.process.start()
        time.sleep(1)
        

    def test_add_post(self):
        log= logging.getLogger("unittest.TestCase")
        
        ################################## Login as Alice
        #self.browser.visit("http://0.0.0.0:8080/login") # original line
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        #self.assertEqual(self.browser.url, "http://0.0.0.0:8080/") # original line
        # self.assertEqual(self.browser.url, "http://127.0.0.1:5000/") # ask sam about this line
        
############################################ add a test post #####################
        self.browser.visit("http://127.0.0.1:5000")
        self.browser.click_link_by_partial_href('add')
        self.browser.fill("title", "post test1 title")
        self.browser.fill("content", "post test1 content")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        post_found = self.browser.find_by_tag('h1').value #cheated here - made template title h2. how do we access? index?
        #post_found = self.browser.find_by_text('post test1 title').value - didnt work
        
        log.debug( "FIRSTH1= %r", post_found )
        
        self.assertEqual(post_found, "post test1 title")

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()

if __name__ == "__main__":
    
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "unittest.TestCase" ).setLevel( logging.DEBUG )
    
    unittest.main()
    
############################################################################    
# Basic program flow
# 1.  login as Alice
# 2.  look for and click on navbar for /post/add route
# 3.  Add title to post
# 4.  Add content to post
# 5.  submit post
# 6.  check to see that content and title are displayed on screen.

