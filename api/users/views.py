from flask import (
    request,
    jsonify,
    Blueprint
)
import uuid
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from api.auth.helper import token_required

# from api.users import views
from api.models import User
from api import db

users_blueprint = Blueprint(
    'users',
    __name__,
    # template_folder='templates'
)


@users_blueprint.route('/', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()

    output = []
    for user in users:
        user_data = {
            'public_id': user.public_id,
            'name': user.name,
            'password': user.password,
            'admin': user.admin
        }
        output.append(user_data)

    return jsonify({'users': output})


@users_blueprint.route('/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No User found!'})

    user_data = {
        'public_id': user.public_id,
        'name': user.name,
        'password': user.password,
        'admin': user.admin
    }

    return jsonify({'user': user_data})


@users_blueprint.route('/', methods=['POST'])
@token_required
def create_user(current_user):
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),
                    name=data['name'], password=hashed_password, admin=False)

    my_object = MyObject()
    db.session.add(my_object)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@users_blueprint.route('/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'Not User found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The User has been promoted!'})


@users_blueprint.route('/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'Not User found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The User has been deleted!'})
