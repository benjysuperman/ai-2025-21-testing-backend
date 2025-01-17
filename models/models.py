import uuid

from database import USERS, TODOS


class User:

    def __init__(self, the_id:int, username:str, password:str,role:str):
        self.id = the_id
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }

    @staticmethod
    def get_users():
        return USERS

    @staticmethod
    def find_by_credentials(username, password):
        users = User.get_users()
        user = None
        for u in users:
            if users[u][1] == username and users[u][2] == password:
                user = users[u]
                break
        return user

    @staticmethod
    def find_by_username(username):
        users = User.get_users()
        user = None
        for u in users:
            if users[u][1] == username:
                user = users[u]
                break
        return user


class Todo:

    def __init__(self, the_id:str, title:str, done:bool,user_id:int):
        self.id = the_id
        self.title = title
        self.done = done
        self.user_id = user_id

    @staticmethod
    def find_all_by_user_id(user_id: int):
        if TODOS[str(user_id)]:
            return TODOS[str(user_id)]
        else:
            return None

    @staticmethod
    def find_by_id(todo_id:str, user_id:int):
        todos = Todo.find_all_by_user_id(user_id)
        todo = None
        for i in range(0,len(todos)):
            if todos[i][0] == todo_id:
                return i
        return todo

    @staticmethod
    def update(t_id, user_id, datas):
        todo_index = Todo.find_by_id(t_id, user_id)
        if todo_index is not None:
            TODOS[str(user_id)][todo_index][1] = datas['title']
            TODOS[str(user_id)][todo_index][2] = (0,1)[datas["done"]]
            todo =  Todo(
                TODOS[str(user_id)][todo_index][0],
                TODOS[str(user_id)][todo_index][1],
                TODOS[str(user_id)][todo_index][2] == 1,
                TODOS[str(user_id)][todo_index][3]
            )
            return todo.to_dict()
        else:
            return None

    @staticmethod
    def add(datas):
        todos = TODOS[str(datas['user_id'])]
        if todos is None:
            todos = []
        new_todo = [str(uuid.uuid4()), datas['title'], (0, 1)[datas['done']], datas['user_id']]
        todo_obj = Todo(new_todo[0], new_todo[1], new_todo[2] == 1, int(new_todo[3]))
        TODOS[str(datas['user_id'])].append(new_todo)
        return todo_obj.to_dict()

    @staticmethod
    def delete(t_id, user_id):
        del TODOS[str(user_id)][Todo.find_by_id(t_id, user_id)]
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "user_id": self.user_id,
        }

