import datetime
import os

import bcrypt
from flask import jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)
from pandas.errors import ParserError
from werkzeug.utils import secure_filename

from db import db
from models import File, User
from utils import get_file_columns


def register_user():
    """
    Register a new user.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.

    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        response = {"message": "User with that username already exists"}
        return jsonify(response), 409

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    response = {"message": "User registered successfully"}
    return jsonify(response), 200


def login_user():
    """
    Authenticate user and generate access token.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.

    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Find the user by username
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        response = {"message": "Invalid username or password"}
        return jsonify(response), 401

    # Verify the password
    if not bcrypt.checkpw(password.encode("utf-8"), existing_user.password):
        response = {"message": "Invalid username or password"}
        return jsonify(response), 401

    # Generate access token

    access_token = create_access_token(
        identity=existing_user.id,
        expires_delta=datetime.timedelta(minutes=60),
    )

    response = {"access_token": access_token}
    return jsonify(response), 200


@jwt_required()
def upload_file():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if "file" not in request.files:
        response = {"message": "No file provided"}
        return jsonify(response), 400

    file = request.files["file"]

    if file.filename == "":
        response = {"message": "Empty filename"}
        return jsonify(response), 400

    if not file.filename.endswith(".csv"):
        response = {
            "message": "Invalid file format. Only CSV files are allowed."
        }
        return jsonify(response), 400

    filename = secure_filename(file.filename)

    # Создание директории, если она не существует
    directory = f"uploads/{current_user.id}"
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, filename)

    file.save(file_path)

    new_file = File(user=current_user, filename=filename, path=file_path)
    db.session.add(new_file)
    db.session.commit()

    response = {"message": "File uploaded successfully"}
    return jsonify(response), 200


@jwt_required()
def get_user_files():
    current_user_id = get_jwt_identity()

    # Получение текущего пользователя из базы данных
    current_user = User.query.get(current_user_id)

    files = current_user.files

    file_list = []
    for file in files:
        try:
            columns = get_file_columns(file.path)

            file_info = {
                "file_id": file.id,
                "filename": file.filename,
                "columns": columns,
            }
            file_list.append(file_info)

        except ParserError as error_message:
            error_message = (
                f"Error reading columns from file '{file.filename}': "
                f"{error_message}"
            )
            file_info = {
                "file_id": file.id,
                "filename": file.filename,
                "columns": [],
                "error": error_message,
            }
            file_list.append(file_info)

    response = {"files": file_list}
    return jsonify(response), 200
