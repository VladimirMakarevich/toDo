import logging

from flask import Flask, request, jsonify

from model import Schema
from service import ToDoService

app = Flask(__name__)

logging.basicConfig(filename='demo.log', level=logging.DEBUG)


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, " \
                                                       "X-Requested-With "
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_world(name):
    return 'Hello ' + name + '!)))'


@app.route("/todo", methods=["GET"])
def list_todo():
    return jsonify(ToDoService().list())


@app.route("/todo", methods=["POST"])
def create_todo():
    json = request.get_json()
    app.logger.info(json)
    return jsonify(ToDoService().create(json))


@app.route("/todo/<item_id>", methods=["PUT"])
def update_item(item_id):
    return jsonify(ToDoService().update(item_id, request.get_json()))


@app.route("/todo/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    return jsonify(ToDoService().delete(item_id))


if __name__ == '__main__':
    Schema()
    app.run(debug=True)
