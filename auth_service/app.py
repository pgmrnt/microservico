from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = 'CODIGO' 
jwt = JWTManager(app)

users = []

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if username and password:
        users.append({'username': username, 'password': password})
        return jsonify({"msg": "Usuário registrado com sucesso!"}), 201
    return jsonify({"msg": "Usuário ou senha não fornecidos!"}), 400


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    
    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Usuário ou senha inválidos!"}), 401


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    app.run(debug=True)

