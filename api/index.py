from datetime import timedelta
from functools import wraps

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, decode_token

from database import db, jwt
from datas.i18n import get_i18n
from models.models import User, Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "zaaa25Tefek58ynbqm658dziPsn"
app.config['JWT_VERIFY_SUB'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=3)
db.init_app(app)
jwt.init_app(app)
CORS(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1] # Assuming format `Bearer <token>`
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        data = get_jwt_identity()
        print(data)
        return f(*args, **kwargs)
    return decorated


@app.route("/api/<lang>/login", methods=["POST"])
def login(lang: str):
    datas = request.get_json()
    if not datas.get('username') or not datas.get("password"):
        return jsonify({"msg": get_i18n(lang, "MISSING_CREDENTIAL")}), 400
    user = User.find_by_credentials(username=datas.get('username'), password=datas.get("password")).first()
    if not user:
        return jsonify({"msg": get_i18n(lang, "WRONG_CREDENTIALS")}), 404
    else:
        return jsonify({
            "user": user.to_dict(),
            "access_token": create_access_token(identity={'username': user.username, 'role': user.role})}), 200


@app.route("/api/<lang>/todos", methods=["GET"])
@jwt_required()
def get_todos(lang: str):
    token = request.headers["Authorization"].replace("Bearer ", "")
    user = User.find_by_username(decode_token(token)["sub"]["username"]).first()
    res = Todo.find_all_by_user_id(user.id)
    todos = []
    for todo in res:
        todos.append(todo.to_dict())
    return jsonify({"todos": todos})

@app.route("/api/<lang>/todos", methods=["POST"])
@jwt_required()
def post_todos(lang: str):
    user = User.find_by_username(get_jwt_identity()["username"]).first()
    json = request.get_json()
    json['user_id'] = user.id
    todo = Todo.add(json)
    return jsonify({"todo": todo})

@app.route("/api/<lang>/todos/<int:todo_id>", methods=["PUT"])
@jwt_required()
def put_todos(lang: str, todo_id: int):

    return jsonify({"todo": Todo.update(todo_id, request.get_json())})

@app.route("/api/<lang>/todos/<int:todo_id>", methods=["DELETE"])
@jwt_required()
def delete_todos(lang: str, todo_id: int):
    user = User.find_by_username(get_jwt_identity()["username"]).first()
    return jsonify({"todo": Todo.delete(todo_id, user.id)})

@app.route("/api/<lang>/contact", methods=["POST"])
@jwt_required()
def submit_contact_form(lang: str):
    print(request.get_json())
    return jsonify({"msg": get_i18n(lang, "EMAIL_SENT")}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
