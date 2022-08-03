from dotenv import load_dotenv
from os import environ
from flask import Flask, redirect, render_template, jsonify, url_for, request
from resources.common_names import common_names
from models.birdobservation import BirdObservation, Db
from resources.check import check_string, check_int, check_float
import gunicorn

# Load environment
load_dotenv('.env')

# Initialize app  Creating heroku-postgresql:hobby-dev on ⬢ safe-lake-35217... free
app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY')

# Initialize DB   Created postgresql-curly-73850 as DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL').replace('postgres://', 'postgresql://') # this is to solve a bug in heroku
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Db.init_app(app)

# # Define birds per page
BIRDS_PER_PAGE = 25
MAX_STRING_LENGTH = 64
POST_OBSERVATION_DEFAULTS = { # All null values! This is just for POST routes!!!
    "ebird_code": None,
    "confidence": None,
    "when_heard": None,
    "device_id": None
}

def get_pages( total, offset = 0, limit = BIRDS_PER_PAGE ):
    pages = { 'begin' : 0 };
    pages[ 'prev' ] = max( offset - limit, 0 ) # don't want a negative index!
    pages[ 'current' ] = min( max( 0, offset ), total ) # gotta be in range!
    pages[ 'next' ] = min( offset + limit, total - limit ) # don't want to go over
    pages[ 'end' ] = total - limit # just get the end.
    return pages

@app.route('/')
def index(messages = [], errors = []):
    return render_template("index.html", messages=messages, errors=errors)

@app.route('/load_data', methods=['GET'])
def load_data():
    observations_json = {'observations': []}
    observations = BirdObservation.query.all()
    for observation in observations:
        observation_info = observation.__dict__
        del observation_info['_sa_instance_state']
        observations_json['observations'].append(observation_info)
    return jsonify(observations_json)

@app.route('/observations', defaults={'offset': 0, 'limit': BIRDS_PER_PAGE}, methods=['GET'])
@app.route('/observations/<offset>', defaults={'limit': BIRDS_PER_PAGE}, methods=['GET'])
@app.route('/observations/<offset>/<limit>', methods=['GET'])
def list(offset, limit, messages=[], errors=[]):
    # get the pagination limits
    # count the total number of records,
    # but this could also return an error! What to do?
    total = BirdObservation.query.count()

    #session['key'] = 'value'

    # sanitize inputs!
    try:
        # get the pagination limits
        total = BirdObservation.query.count()  # count the total number of records

        # check the values
        offset = check_int(offset, "offset", 0, total)
        limit = check_int(limit, "limit", 1)  # don't care about how long limit is so long as it's greater than 1

        # get just the observations we want to show
        observations = BirdObservation.query.offset(offset).limit(limit)

        # paginate
        pages = get_pages(total, offset, limit)

        common_names_display = [common_names[observation.ebird_code] for observation in observations]

        errors.clear()
        messages.clear()

        # return the list
        return render_template("list.html", observations=zip(observations, common_names_display),
                               pages=pages, limit=limit, messages=messages, errors=errors)
    except Exception as e:
        # get the observations (don't need offset)
        observations = BirdObservation.query.limit(BIRDS_PER_PAGE)

        # paginate
        pages = get_pages(total, 0, BIRDS_PER_PAGE)

        # get the error message
        errors.clear()
        errors.append(e.message if hasattr(e, 'message') else e)

        return redirect('/observations')

@app.route('/latest', methods=['GET'])
def show_latest(messages=[], errors=[]):  # so we don't have to redirect!!!
    # HW: Sanitize the input!
    try:
        # sanitize
        # get the latest
        latest = BirdObservation.query.order_by(BirdObservation.obs_id.desc()).filter_by().first()
        if latest is None:
            raise LookupError(f'No records in the database')

        # show the observations
        return render_template('latest.html', latest=latest, common_name=common_names[latest.ebird_code],
                               messages=messages)
    except Exception as e:
        # get error
        errors.clear()
        errors.append(e.message if hasattr(e, 'message') else e)

        # go back to the list
        return list(0, BIRDS_PER_PAGE, errors=errors)


# CRUD - delete
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#deleting-records
# E.g. /observation/delete/101
@app.route('/observation/delete/<obs_id>')
def delete_observation(obs_id, messages=[], errors=[]):
    # HW: Sanitize the input!
    try:
        messages.clear()
        errors.clear()

        # get the observation
        observation = BirdObservation.query.filter_by( obs_id = obs_id ).first()
        if not observation:
            raise LookupError( f'Observation {obs_id} does not exist!' )

        # delete this observation
        Db.session.delete( observation )

        # commit to db
        Db.session.commit()

        # send a message
        messages.append( f'Observation {obs_id} deleted successfully' )

        # show the list
        return list( 0, BIRDS_PER_PAGE, messages )
    except Exception as e:
        # get error
        errors.append( e.message if hasattr(e, 'message') else e )

        # go back to the list
        return redirect('/observations')

