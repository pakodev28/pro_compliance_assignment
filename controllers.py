import datetime
import os
from io import BytesIO

import bcrypt
from flask import jsonify, request, send_file
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from pandas.errors import ParserError
import pandas as pd
from werkzeug.utils import secure_filename

from db import db
from models import File, User
from utils import get_file_columns, sort_data, filter_data


def register_user():
    """
    Register a new user.

    Returns:
        tuple: A tuple containing message that User registered successfully
        and the HTTP status code.

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
        tuple: A tuple containing the JSON response(access_token)
        and the HTTP status code.

    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        response = {"message": "Invalid username or password"}
        return jsonify(response), 401

    if not bcrypt.checkpw(password.encode("utf-8"), existing_user.password):
        response = {"message": "Invalid username or password"}
        return jsonify(response), 401

    access_token = create_access_token(
        identity=existing_user.id,
        expires_delta=datetime.timedelta(minutes=60),
    )

    response = {"access_token": access_token}
    return jsonify(response), 200


@jwt_required()
def upload_file():
    """
    Uploads a file for the current user.

    Returns:
        tuple:
        JSON response: Message that the file has been uploaded successfully.
        And the HTTP status code.
    """
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
    """
    Retrieves the files of the current user with column information.

    Returns:
        tuple:
        JSON response: Response containing the user's files
        and their column information. And the HTTP status code.
    """
    current_user_id = get_jwt_identity()

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


@jwt_required()
def delete_file(file_id):
    """
    Deletes a file owned by the current user.

    Params:
        file_id: The ID of the file to delete.

    Returns:
        tuple:
        JSON response: Message that the file has been deleted successfully.
        And the HTTP status code.
    """
    current_user_id = get_jwt_identity()

    current_user = User.query.get(current_user_id)

    file = File.query.filter_by(id=file_id, user=current_user).first()

    if not file:
        response = {
            "message": "File not found or does not belong to the current user"
        }
        return jsonify(response), 404

    if os.path.exists(file.path):
        os.remove(file.path)

    db.session.delete(file)
    db.session.commit()

    response = {"message": "File deleted successfully"}
    return jsonify(response), 200


@jwt_required()
def get_file_data_by_id(file_id):
    """
    Retrieves the file based on the file ID
    (optional sort and filtering).

    Details:
        - Checks file existence and user's access.
        - Returns the source file as a CSV attachment if no filters or sort.
        - Applies filters using filter_data() if filters are provided.
        - Sorts data using sort_data() if sort columns are provided.
        - Converts DataFrame data to CSV string encoded in bytes
          and return modified file.
    """
    current_user_id = get_jwt_identity()

    file = File.query.filter_by(id=file_id, user_id=current_user_id).first()
    if not file:
        response = {"message": "File not found or access denied"}
        return jsonify(response), 404
    filters = request.args.get("filters")

    sort_columns = request.args.get("sort_columns")

    if not filters and not sort_columns:
        return send_file(
            file.path,
            mimetype="text/csv",
            as_attachment=True,
            download_name=file.filename,
        )

    df = pd.read_csv(file.path)

    if filters:
        conditions = [filter.split("__") for filter in filters.split(",")]
        df = filter_data(df, conditions)

    if sort_columns:
        columns = []
        ascending = []
        sort_params = sort_columns.split(",")
        for param in sort_params:
            column_parts = param.split(":")
            if len(column_parts) != 2:
                response = {"message": "Invalid sort_columns format"}
                return jsonify(response), 400
            column_name = column_parts[0]
            column_ascending = column_parts[1].lower() == "true"
            columns.append(column_name)
            ascending.append(column_ascending)
        df = sort_data(df, columns, ascending)

    csv_data = df.to_csv(index=False)
    csv_bytes = csv_data.encode("utf-8")

    return send_file(
        BytesIO(csv_bytes),
        mimetype="text/csv",
        as_attachment=True,
        download_name=file.filename,
    )
