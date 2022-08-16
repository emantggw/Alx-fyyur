from flask import Blueprint, flash, redirect, render_template, request, url_for
from forms import ShowForm
from models.models import Artist, Venue, db, Show
from datetime import datetime

show_controller = Blueprint('show_controller', __name__, template_folder='templates')

@show_controller.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  shows_data = []
  for show in shows:
    show_info = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": str(show.start_time)
    }
    current_time = datetime.now()
    if current_time > show.start_time:
      shows_data.append(show_info)

  return render_template('pages/shows.html', shows=shows_data)

@show_controller.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@show_controller.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  if form.validate():
    start_time = get_time_date_format(request.form['start_time']) 
    show = Show(artist_id=form.artist_id.data, venue_id=form.venue_id.data, start_time=start_time)
    try:
      db.session.add(show)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
    except:
      db.session.rollback()
      # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Show could not be listed.')
    finally:
      db.session.close()
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return redirect(url_for('index'))
  flash('Invalid input.')
  return render_template('pages/home.html')

def get_time_date_format(str):
  start_time = str.split(' ')
  date_time = start_time[0].split('-')
  date_time += start_time[1].split(':')
  for i in range(len(date_time)):
    date_time[i] = int(date_time[i])
  start_time = datetime(date_time[0], date_time[1], date_time[2], date_time[3], date_time[4], date_time[5])
  return start_time
