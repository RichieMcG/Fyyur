#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Venue, Artist, Show

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Helper functions.
#----------------------------------------------------------------------------#

def shows_data_format(pastUpcoming, shows_data):
  '''Sorts shows_data into past and upcoming, parses the time, formats data'''
  data = []
  for show in shows_data:
    if pastUpcoming == 'upcoming':
     if show.start_time > datetime.now():
       data.append({
         "artist_id": show.artist_id,
          "artist_name": show.artist.name,
          "venue_name": show.venue.name,
          "artist_image_link": show.artist.image_link,
          "venue_image_link": show.venue.image_link,
          "start_time": format_datetime(str(show.start_time))
       })
    else:
      if show.start_time < datetime.now():
       data.append({
         "artist_id": show.artist_id,
          "artist_name": show.artist.name,
          "venue_name": show.venue.name,
          "artist_image_link": show.artist.image_link,
          "venue_image_link": show.venue.image_link,
          "start_time": format_datetime(str(show.start_time))
       })
  return data

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  error = False
  '''Retrieves all venue data and formats it grouped by city and state'''
  areas = db.session.query(Venue.city, Venue.state).distinct()
  result = []
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  try:
    for area in areas:
      area = dict(zip(('city', 'state'), area))
      area['venues'] = []
      for venue in Venue.query.filter_by(
              city=area['city'],
              state=area['state']
          ).all():
          upcoming_shows = Show.query.filter_by(
                  venue_id=venue.id
              ).filter(
                Show.start_time > now
              ).all()
          venue_data = {
              'id': venue.id,
              'name': venue.name,
              'num_upcoming_shows': len(upcoming_shows)
          }
          area['venues'].append(venue_data)
      result.append(area)
  except:
    error = True
    print('An error occured retriving and formating the venue data')
  finally:
    if error:
      abort(500)
    else:
      return render_template('pages/venues.html', areas=result)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  search_results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).with_entities(Venue.id, Venue.name).all()
  response = {
    "count": len(search_results),
    "data": []
  }
  for result in search_results:
      show_count = Show.query.filter_by(venue_id=result.id).filter(Show.start_time > datetime.now()).count()
      data = {
          "id": result.id,
          "name": result.name,
          "num_upcoming_shows": show_count,
      }
      response['data'].append(data)
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  ''' shows the venue page with the given venue_id '''

  error=False
  try:
    venue = Venue.query.get(venue_id)
    shows_data = Show.query.filter_by(venue_id=venue.id).all()
    past_shows = shows_data_format('past', shows_data)
    upcoming_shows = shows_data_format('upcoming', shows_data)
    data = venue.format()
    data['upcoming_shows'] = upcoming_shows
    data['past_shows'] = past_shows
    data['upcoming_shows_count'] = len(upcoming_shows)
    data['past_shows_count'] = len(past_shows)
    
  except:
    error=True
  finally:
    if (error):
      return abort(404)
    else:
      return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    form = VenueForm()
    venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      genres=form.genres.data,
      facebook_link=form.facebook_link.data,
      website=form.website.data,
      image_link=form.image_link.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data,
    )
    venue.insert()

    flash('Venue ' + request.form['name'] + ' was successfully listed!', 'success')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.', 'error')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    venue.delete()

    flash('The venue ' + venue.name + 'has been successfully deleted!', 'success')
  except:
    db.session.rollback()
    flash('The venue ' + venue.name + 'could not be deleted!', 'error')
  finally:
    db.session.close()
  return render_template('pages/venues.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists_data=Artist.query.all()
  return render_template('pages/artists.html', artists=artists_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  search_results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).with_entities(Artist.id, Artist.name).all()
  response = {
    "count": len(search_results),
    "data": []
  }
  for result in search_results:
      show_count = Show.query.filter_by(artist_id=result.id).filter(Show.start_time > datetime.now()).count()
      data = {
          "id": result.id,
          "name": result.name,
          "num_upcoming_shows": show_count,
      }
      response['data'].append(data)

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  '''shows the venue page with the given venue_id'''

  artist = Artist.query.get(artist_id)
  shows_data = Show.query.join(
    Artist, Artist.id == Show.artist_id
    ).join(
      Venue, Show.venue_id == Venue.id
      ).filter(
        Show.artist_id==artist.id
        ).all()
  past_shows = shows_data_format('past', shows_data)
  upcoming_shows = shows_data_format('upcoming', shows_data)

  data = artist.format()
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)
 
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist_data = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist_data)
  return render_template('forms/edit_artist.html', form=form, artist=artist_data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    form = ArtistForm()

    artist = Artist.query.get(artist_id)
    
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = form.genres.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    artist.facebook_link = form.facebook_link.data
    artist.website = form.website.data
    artist.image_link = form.image_link.data
    artist.update()
    flash('The Artist ' + request.form['name'] + ' was updated.', 'success')
  except:
    db.session.rollback()
    flash('An error occurred. The Artist ' + request.form['name'] + ' could not be updated.', 'error')
  finally:
    db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue_data = Venue.query.get(venue_id)
  form = VenueForm(obj=venue_data)
  return render_template('forms/edit_venue.html', form=form, venue=venue_data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    form = VenueForm()

    venue = Venue.query.get(venue_id)

    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.phone = form.phone.data
    venue.genres = form.genres.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    venue.facebook_link = form.facebook_link.data
    venue.website = form.website.data
    venue.image_link = form.image_link.data

    venue.update()
    flash('The Venue' + request.form['name'] + ' was updated', 'success')
  except:
    db.session.rollback()
    flash('An error occurred. The Venue ' + request.form['name'] + ' could not be updated.', 'error')
  finally:
    db.session.close()
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm()
  try:
    artist = Artist(
      name = form.name.data,
      city = form.city.data,
      state = form.state.data,
      phone=form.phone.data, 
      genres = form.genres.data,
      seeking_venue=form.seeking_venue.data,
      seeking_description = form.seeking_description.data,
      facebook_link =form.facebook_link.data,
      image_link = form.image_link.data,
      website = form.website.data,
    )

    artist.insert()
    flash('Artist ' + request.form['name'] + ' was successfully added!', 'success')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be added.', 'error')
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data=[]
  shows = Show.query.join(Artist, Artist.id == Show.artist_id).join(Venue, Show.venue_id == Venue.id).all()
  for show in shows:
    print(show.artist.name)
    show_data = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": str(show.start_time)
    }
    data.append(show_data)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()

  try:
    show = Show(
      venue_id=form.venue_id.data,
      artist_id=form.artist_id.data,
      start_time=form.start_time.data
    )
    show.insert()
    flash('Show was successfully listed!', 'success')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.', 'error')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return  render_template('errors/500.html'), 500


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
