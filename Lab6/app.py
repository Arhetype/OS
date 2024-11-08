from flask import Flask, request, jsonify, render_template
import jwt
import os
import logging
from functools import wraps

app = Flask(__name__)

# Секретный ключ для создания и проверки JWT токенов
SECRET_KEY = "secret_key"

# Словарь для хранения пользователей и их данных
USERS = {
    "admin": {
        "password": "admin_password",
        "role": "admin",
        "certificate": "admin_certificate"
    },
    "user": {
        "password": "user_password",
        "role": "user",
        "certificate": None
    }
}

# Настройка логирования
logging.basicConfig(filename='security.log', level=logging.INFO)

# Проверка размера файла
def check_file_size(file):
    return os.path.getsize(file) <= 30 * 1024  # 30 КБ

# Аутентификация пользователя
def authenticate(username, password, certificate=None):
    user = USERS.get(username)
    if user:
        if user['role'] == 'admin' and certificate != user['certificate']:
            return None
        if user['password'] == password:
            return user
    return None

# Создание JWT токена
def create_jwt_token(user):
    token = jwt.encode({"user": user['role']}, SECRET_KEY, algorithm="HS256")
    return token

# Декоратор для проверки JWT токена
def jwt_required(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": "Token is missing"}), 401

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user_role = payload["user"]
                if role and user_role != role:
                    return jsonify({"error": "Access denied"}), 403
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

        return wrapper

    return decorator

# Главная страница с формой регистрации
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')
        certificate = data.get('certificate')

        if username in USERS:
            return jsonify({"error": "User already exists"}), 400

        USERS[username] = {
            "password": password,
            "role": role,
            "certificate": certificate
        }

        return jsonify({"message": "User registered successfully"}), 201

    return '''
    <form method="post">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <div>
            <label for="role">Role:</label>
            <select id="role" name="role">
                <option value="admin">Admin</option>
                <option value="user" selected>User</option>
            </select>
        </div>
        <div>
            <label for="certificate">Certificate:</label>
            <input type="text" id="certificate" name="certificate">
        </div>
        <div>
            <input type="submit" value="Register">
        </div>
    </form>
    '''

# Аутентификация пользователя и создание JWT токена
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    certificate = data.get('certificate')

    user = authenticate(username, password, certificate)
    if user:
        token = create_jwt_token(user)
        return jsonify({"token": token.decode('utf-8')})
    else:
        return jsonify({"error": "Invalid credentials"}), 401



# Загрузка файла
@app.route('/upload', methods=['POST'])
@jwt_required(role='user')
def upload_file():
    file = request.files['file']
    if file and check_file_size(file):
        file.save(os.path.join('uploads', file.filename))
        logging.info(f"User {request.headers.get('Authorization')} uploaded file: {file.filename}")
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "File size exceeds the limit (30 KB)"}), 400

# Урезанный функционал для пользователя User
@app.route('/restricted', methods=['GET'])
@jwt_required(role='user')
def restricted_function():
    return jsonify({"message": "This is restricted function for User"}), 200

# Полный функционал для пользователя Admin
@app.route('/admin', methods=['GET'])
@jwt_required(role='admin')
def admin_function():
    return jsonify({"message": "This is full functional for Admin"}), 200

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
