from flask import Flask
from db import db, jwt
from resources.packages import package_bp
from resources.users import user_bp
from resources.booking import booking_bp
import jwt_error_handlers
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///travel-website.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(package_bp, url_prefix='/package')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(booking_bp, url_prefix='/booking')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)