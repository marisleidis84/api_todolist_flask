from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Todo
import json


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:leidy123@localhost:3306/api_todo'
db.init_app(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/todos/username/<username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def todos(username):

    if request.method == 'GET':
        todos = Todo.query.filter_by(username=username).first()
        if not todos:
            return jsonify({"msg": "user not found"}), 404

        return jsonify(todos.serialize()), 200


    if request.method == 'POST':
        body = request.get_json()
        if type(body) != list:
            return jsonify({"msg": "type not found"}), 400

        body.append({
            "label": "sample task",
            "done": "false"
        })

        todo = Todo() # instancia de la clase Todo de models
        todo.username = username # Aqui estoy asignamdo el suario del input a la colmna username de todo
        todo.tasks = json.dumps(body)
        todo.save()
        return jsonify({"result": "ok"}), 201
    
    if request.method == 'PUT':
        body = request.get_json()
        todos = Todo.query.filter_by(username=username).first()
        if todos:
            todos.tasks = json.dumps(body)
            todos.update()
            return jsonify({"msg": "a list with " + str(len(body)) + " todos was successfully saved" }), 200
        else:
            return jsonify({"msg": "type not found"}), 400
        

    if request.method == 'DELETE':
        todos = Todo.query.filter_by(username=username).first()
        if not todos:
            return jsonify({"msg": "type not found"}), 404
        todos.delete()
        return jsonify({"result": "ok"}), 200   

if __name__ == '__main__':
    manager.run()
