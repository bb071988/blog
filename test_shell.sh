#SQLALCHEMY_DATABASE_URI="postgresql://ubuntu:action@localhost:5432/blogful-test"
#echo SECRET_KEY="Not secret"
#PYTHONPATH=. python blog/tests/test_views_integration.py

echo CONFIG_PATH="blog.config.TestingConfig"
PYTHONPATH=. python blog/tests/test_views_integration.py