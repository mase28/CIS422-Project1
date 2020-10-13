
"""Creates the application object as an instance
   of class Flask imported from the flask package"""

from flask import Flask

app = Flask(__name__)    # instance of class Flask in the __init__.py script

from app import routes   # Bottom import is a workaround to circular imports