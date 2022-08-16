"""
CREDITS: @mahmoud-sharshar github
"""

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from forms import *
from models.models import  db
from controllers.artist_controller import artist_controller
from controllers.show_controller import show_controller
from controllers.venue_controller import venue_controller

app = Flask(__name__)
moment = Moment(app)

app.config.from_object('config')

# Controllers
app.register_blueprint(artist_controller)
app.register_blueprint(show_controller)
app.register_blueprint(venue_controller)

# Initing db from Models
db.init_app(app)

migrate = Migrate(app, db)

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

@app.route('/')
def index():
  return render_template('pages/home.html')
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404
@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
