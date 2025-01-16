from database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10))  # 'writer' or 'viewer'
    todos = db.relationship('Todo', backref='user', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }

    @staticmethod
    def find_by_credentials(username, password):
        return User.query.filter_by(username=username, password=password)

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username)


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @staticmethod
    def find_all_by_user_id(user_id: int):
        return Todo.query.filter_by(user_id=user_id)

    @staticmethod
    def find_by_id(todo_id: int):
        return Todo.query.filter_by(id=todo_id)

    @staticmethod
    def update(t_id, datas):
        todo = Todo.find_by_id(t_id).first()
        todo.title = datas["title"]
        todo.done = datas["done"]
        db.session.commit()
        return todo.to_dict()

    @staticmethod
    def add(datas):
        todo = Todo()
        todo.title = datas['title']
        todo.done = datas['done']
        todo.user_id = datas['user_id']
        db.session.add(todo)
        db.session.commit()
        return todo.to_dict()

    @staticmethod
    def delete(t_id, user_id):
        todo = Todo.find_by_id(t_id).filter_by(user_id=user_id).first()
        db.session.delete(todo)
        db.session.commit()
        return todo.to_dict()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "user_id": self.user_id,
        }
