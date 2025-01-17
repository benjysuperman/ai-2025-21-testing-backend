import uuid

from flask_jwt_extended import JWTManager

USERS = {
    "1": ['1',"admin","1234","admin"],
    "2": ['2',"writer","1234","writer"],
    "3": ['3',"reader","1234","reader"],
    "4": ['4',"natalia","1234","admin"],
}

TODOS = {
    "1": [[str(uuid.uuid4()),"Test",0,1]],
    "2": [],
    "3": [],
    "4": [],
}

jwt = JWTManager()
