from flask import (
    Blueprint,
    request,
    jsonify,
    make_response
)
import uuid
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
import jwt
from datetime import datetime, timedelta
from functools import wraps

from api.models import User
from api import app, db

auth_blueprint = Blueprint(
    'auth',
    __name__,
    # template_folder='templates'
)


@auth_blueprint.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id,
                            'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
