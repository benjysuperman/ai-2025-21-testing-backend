import uuid

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
        with open("datas/users.txt", "r") as f:
            content = f.read()
            users = content.strip().split("\n")
            for i in range(0,len(users)):
                users[i] = users[i].split("|")
        return users

    @staticmethod
    def find_by_credentials(username, password):
        users = User.get_users()
        user = None
        for u in users:
            if u[1] == username and u[2] == password:
                user = u
                break
        return user

    @staticmethod
    def find_by_username(username):
        users = User.get_users()
        user = None
        for u in users:
            if u[1] == username:
                user = u
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
        try:
            with open(f"datas/todos-{user_id}.txt", "r") as f:
                content = f.read().strip()
                if content != '':
                    todos = content.strip().split("\n")
                    for i in range(0, len(todos)):
                        todos[i] = todos[i].split("|")
                else:
                    return None
        except FileNotFoundError:
            with open(f"/api/datas/todos-{user_id}.txt", "w") as f:
                f.write("")
            todos = []
        return todos

    @staticmethod
    def find_by_id(todo_id:str, user_id:int):
        todos = Todo.find_all_by_user_id(user_id)
        todo = None
        for i in range(0,len(todos)):
            if todos[i][0] == todo_id:
                todo = Todo(todos[i][0], todos[i][1],todos[i][2] == '1', int(todos[i][3]))
                break
        return todo

    @staticmethod
    def update(t_id, user_id, datas):
        todo_to_save = Todo.find_by_id(t_id, user_id)
        if todo_to_save is not None:
            todos = Todo.find_all_by_user_id(user_id)
            todo_to_save.title = datas["title"]
            todo_to_save.done = (0,1)[datas["done"]]
            with open(f"/api/datas/todos-{user_id}.txt", "w") as f:
                content = ""
                for todo in todos:
                    if todo[0] == todo_to_save.id:
                        content += f"{todo_to_save.id}|{todo_to_save.title}|{(0,1)[todo_to_save.done]}|{todo_to_save.user_id}\n"
                    else:
                        content += f"{todo[0]}|{todo[1]}|{todo[2]}|{todo[3]}\n"
                f.write(content.strip())
            return todo_to_save.to_dict()
        else:
            return None

    @staticmethod
    def add(datas):
        todos = Todo.find_all_by_user_id(datas['user_id'])
        if todos is None:
            todos = []
        with open(f"/api/datas/todos-{datas['user_id']}.txt", "w") as f:
            new_todo = [str(uuid.uuid4()), datas['title'], ('0', '1')[datas['done']], str(datas['user_id'])]
            todo_obj = Todo(new_todo[0], new_todo[1], new_todo[2] == '1', int(new_todo[3]))
            todos.append(new_todo)
            content = ""
            for todo in todos:
                content += f"{todo[0]}|{todo[1]}|{todo[2]}|{todo[3]}\n"
            f.write(content.strip())
        return todo_obj.to_dict()

    @staticmethod
    def delete(t_id, user_id):
        todos = Todo.find_all_by_user_id(user_id)
        with open(f"/api/datas/todos-{user_id}.txt", "w") as f:
            content = ""
            for t in todos:
                if t[0] != t_id:
                    content += f"{t[0]}|{t[1]}|{t[2]}|{t[3]}\n"
            f.write(content)
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "user_id": self.user_id,
        }
