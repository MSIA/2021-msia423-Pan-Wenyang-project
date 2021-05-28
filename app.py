import traceback
import logging.config
from flask import Flask
from flask import render_template, request, redirect, url_for

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database session
from src.manage_pokemon import PokemonManager, Pokemon

pokemon_manager = PokemonManager(app)


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form.to_dict()['pokemon_name']
        print(form_data)
        try:
            pokemons = pokemon_manager.session.query(Pokemon).filter_by(input=form_data).limit(
                app.config["MAX_ROWS_SHOW"]).all()
            logger.debug("Index page accessed")
            return render_template('index.html', pokemons=pokemons, user_input=form_data)
        except:
            traceback.print_exc()
            logger.warning("Not able to display tracks, error page returned")
            return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
