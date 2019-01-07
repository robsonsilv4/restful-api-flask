from flask import (
    Blueprint
)

from flask import (
    Flask,
    request,
    jsonify,
    make_response
)

from api.models import User
from api import db

todos_blueprint = Blueprint(
    'todos',
    __name__,
    # template_folder='templates'
)


@todos_blueprint.route('/', methods=['GET'])
@token_required
def get_all_todos(current_user):
    todos = Todo.query.filter_by(user_id=current_user.id).all()

    output = []
    for todo in todos:
        todo_data = {
            'id': todo.id,
            'text': todo.text,
            'complete': todo.complete
        }
        output.append(todo_data)

    return jsonify({'todos': output})


@todos_blueprint.route('/<todo_id>', methods=['GET'])
@token_required
def get_one_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if not todo:
        return jsonify({'message': 'No Todo found'})

    todo_data = {
        'id': todo.id,
        'text': todo.text,
        'complete': todo.complete
    }

    return jsonify(todo_data)


@todos_blueprint.route('/', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()

    new_todo = Todo(text=data['text'], complete=False, user_id=current_user.id)

    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Todo created!'})


@todos_blueprint.route('/<todo_id>', methods=['PUT'])
@token_required
def complete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if not todo:
        return jsonify({'message': 'No Todo found'})

    todo.complete = True
    db.session.commit()

    return jsonify({'message': 'Todo item has been completed!'})


@todos_blueprint.route('/<todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if not todo:
        return jsonify({'message': 'No Todo found'})

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo item deleted!'})
