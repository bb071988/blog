createdb blogful-test -O postgres

export NEW_VAR="Testing export"  - sets a new environment variable.

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:action@localhost:5432/blogful-test"
    #SQLALCHEMY_DATABASE_URI = "postgresql://postgres: @localhost:5432/blogful-test"
    DEBUG = False
    SECRET_KEY = "Not secret"

SQLALCHEMY_DATABASE_URI="postgresql://ubuntu:action@localhost:5432/blogful-test"
echo SECRET_KEY="Not secret"
PYTHONPATH=. python blog/tests/test_views_integration.py

