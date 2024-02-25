"""Flask import"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(error):
    """ close the current session"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host=environ["HBNB_API_HOST"],
            port=environ["HBNB_API_PORT"], threaded=True)
