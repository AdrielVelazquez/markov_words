from flask.ext.api import FlaskAPI

app = FlaskAPI(__name__)

from app import routes

from routes import quiz

app.register_blueprint(quiz)