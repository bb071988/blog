import os
class DevelopmentConfig(object):
  ##  SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/blogful" ## from original exercise
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:action@localhost:5432/blogful"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "secretpassword1988")
    
### Adding testing config class for lesson 5.2

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:action@localhost:5432/blogful-test"
    DEBUG = False
    SECRET_KEY = "Not secret"
    
class TravisConfig(object):
    #SQLALCHEMY_DATABASE_URI = "postgresql://postgres:@localhost:5432/blogful-test"
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/blogful-test"
    DEBUG = False
    SECRET_KEY = "Not secret"
    
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/blogful-test"
    
   