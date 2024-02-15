import faker
from flask import Blueprint, jsonify, request
from db import db, token_block_list
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity


user_bp = Blueprint('users', __name__)
faker = faker.Faker()

@user_bp.route('/register', methods=['POST'])
def register_user():
    user_data = request.get_json()

    userName = user_data.get('userName', faker.name())
    userPassword = user_data.get('userPassword', faker.password())
    userEmail = user_data.get('userEmail', faker.email())

    user = User.query.filter_by(userEmail=userEmail).first()

    if user:
        return jsonify({'message': 'User already exists with this email.'}), 400
    
    new_user = User(
        userName = userName,
        userEmail = userEmail,
        userPassword=generate_password_hash(userPassword)
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
            'message': 'New user created', 
            'user': new_user.serialize()
        }), 201


@user_bp.route('/login', methods=['POST'])
def login():
    user_data = request.get_json()

    userEmail = user_data.get('userEmail')
    userPassword = user_data.get('userPassword')

    user = User.query.filter_by(userEmail=userEmail).first()

    if user and check_password_hash(user.userPassword, userPassword):
        return jsonify({
            "message": "User logged in",
            "access_token": create_access_token(identity=user.userEmail),
            "refresh_token": create_refresh_token(identity=user.userEmail)
        }), 200
    
    return jsonify({
        "message": "User not found"
        }), 401


@user_bp.route('/whoami', methods=['GET'])
@jwt_required()
def whoami():
    userEmail = get_jwt_identity()
    user = User.query.filter_by(userEmail=userEmail).first()
    return jsonify({'message': 'Hello, {}'.format(user.userName)}), 200


@user_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    userEmail = get_jwt_identity()
    return jsonify({
        "message": "User refreshed",
        "access_token": create_access_token(identity=userEmail)
    }), 200

@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt().get('jti')
    token_block_list.add(jti)
    return jsonify({
        "message": "User logged out successfully"
    }), 200