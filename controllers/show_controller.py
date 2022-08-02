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
    if show.upcoming:
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
  show = Show()
  show.artist_id = request.form['artist_id']
  show.venue_id = request.form['venue_id']
  start_time = request.form['start_time'].split(' ')
  date_time = start_time[0].split('-')
  date_time += start_time[1].split(':')

  for i in range(len(date_time)):
    date_time[i] = int(date_time[i])
  
  now = datetime.now()
  show.start_time = datetime(date_time[0], date_time[1], date_time[2], date_time[3], date_time[4], date_time[5])
  show.upcoming= (now < show.start_time)

  try:
    db.session.add(show)
    artist = Artist.query.get(show.artist_id)
    venue = Venue.query.get(show.venue_id)
    if show.upcoming:
      artist.upcoming_shows_count += 1
      venue.upcoming_shows_count += 1
    else:
      artist.past_shows_count += 1
      venue.past_shows_count += 1

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
