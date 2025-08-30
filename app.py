from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import bcrypt

from models.meal import Meal
from models.user import User
from database import db


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@127.0.0.1:3306/daily-diet-db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso!"})

    return jsonify({"message": "Credenciais inválidas"}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})

@app.route('/user', methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"})

    return jsonify({"message": "Dados inválidos"}), 400

@app.route('/meal', methods=["POST"])
@login_required
def create_meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    is_on_diet = data.get("is_on_diet")

    if name and description and is_on_diet is not None:
        meal = Meal(name=name, description=description, is_on_diet=is_on_diet, user_id=current_user.id)
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Receita cadastrada com sucesso"}), 201

    return jsonify({"message": "Dados inválidos"}), 400

if __name__ == '__main__':
    app.run(debug=True)