import flask
from flask import request, jsonify

from database import execute

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Create
@app.route('/user', methods=['POST'])
def post():
  user = request.get_json()
  _name = user['name']
  _pwd = user['password']
  _mail = user['email']

  sql = f"INSERT INTO user (name, password, email) VALUES ('{_name}', '{_pwd}', '{_mail}');"

  result = execute(sql, False)
  user['id'] = result.lastrowid
  return jsonify(user)

# Read
# List all users
@app.route('/users', methods=['GET'])
def get_users():
  _id = request.args['id'] if 'id' in request.args else 0
  _name = request.args['name'] if 'name' in request.args else ''
  _pwd = request.args['password'] if 'password' in request.args else ''
  _mail = request.args['email'] if 'email' in request.args else ''

  sql = f"""SELECT * FROM user WHERE 
          ({_id} = 0 OR id = {_id}) 
          AND ('{_name}' = '' OR UPPER(name) = UPPER('{_name}'))
          AND ('{_pwd}' = '' OR UPPER(password) = UPPER('{_pwd}'))
          AND ('{_mail}' = '' OR UPPER(email) = UPPER('{_mail}'));"""

  users = execute(sql)
  return jsonify(users)

# Update
@app.route('/user', methods=['PUT'])
def put():
  user = request.get_json()
  _id = user['id']
  _name = user['name']
  _pwd = user['password']
  _mail = user['email']

  sql = f"UPDATE user SET name='{_name}', password='{_pwd}', email='{_mail}' WHERE id = {_id};"
  execute(sql, False)
  return {}

# Delete
@app.route('/user/<_id>', methods=['DELETE'])
def delete(_id):
  sql = f"DELETE FROM user WHERE id={int(_id)};"
  execute(sql, False)
  return {}


app.run()