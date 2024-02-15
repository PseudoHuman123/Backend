import faker
from flask import Blueprint, jsonify, request
from models import Package, PackageImage
from db import db
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

package_bp = Blueprint('packages', __name__)
faker = faker.Faker()


@package_bp.route('/show', methods=['GET'])
@jwt_required()
def get_packages():
    all_packages = Package.query.all()
    return jsonify([package.serialize() for package in all_packages])


@package_bp.route('/show/<package_id>', methods=['GET'])
def get_package(package_id):
    travel_package = Package.query.filter_by(packageId=package_id).first()
    if not travel_package:
        return jsonify({'message': 'Travel package does not exist'}), 404
    return jsonify(travel_package.serialize())



@package_bp.route('/add', methods=['POST'])
@jwt_required()
def add_package():

    if not get_jwt().get('is_admin', False):
        return jsonify({'message': 'Admin access required'}), 403
    
    travel_data = request.get_json()

    packageName = travel_data.get('packageName', faker.name())
    packageDescription = travel_data.get('packageDescription', faker.paragraph())
    packageDuration = travel_data.get('packageDuration', faker.random_int(min=1, max=10))
    packageCost = travel_data.get('packageCost', faker.random_int(min=1, max=100))
    packageSlots = travel_data.get('packageSlots', faker.random_int(min=1, max=10))

    travel_package = Package.query.filter_by(packageName=packageName).first()
    if travel_package:
        return jsonify({'message': 'Travel package already exists'}), 400


    new_package = Package(
                        packageName = packageName, 
                        packageDescription = packageDescription,
                        packageDuration = packageDuration,
                        packageCost = packageCost,
                        packageSlots = packageSlots
                    )
    
    db.session.add(new_package)
    db.session.commit()


    return jsonify({'message': 'Travel package added successfully'}, 
                   'package', new_package.serialize()), 201



@package_bp.route('/update/<package_id>', methods=['PUT'])
@jwt_required()
def update_package(package_id):
    travel_data = request.get_json()

    if not get_jwt().get('is_admin', False):
        return jsonify({'message': 'Admin access required'}), 403

    package = Package.query.filter_by(packageId=package_id).first()
    if not package:
        return jsonify({'message': 'Travel package does not exist'}), 400
    

    package.packageName = travel_data.get('packageName', package.packageName)
    package.packageDescription = travel_data.get('packageDescription', package.packageDescription)
    package.packageDuration = travel_data.get('packageDuration', package.packageDuration)
    package.packageCost = travel_data.get('packageCost', package.packageCost)
    package.packageSlots = travel_data.get('packageSlots', package.packageSlots)

    db.session.commit()
    return jsonify({'message': 'Travel package updated successfully'}, 'package', package.serialize()), 200



@package_bp.route('/delete/<package_id>', methods=['DELETE'])
@jwt_required()
def delete_package(package_id):
    print(package_id)
    if not get_jwt().get('is_admin', False):
        return jsonify({'message': 'Admin access required'}), 403
    
    package = Package.query.filter_by(packageId=package_id).first()
    if not package:
        return jsonify({'message': 'Travel package does not exist'}), 400
    db.session.delete(package)
    db.session.commit()
    return jsonify({'message': 'Travel package Delted'}), 200


@package_bp.route('/<package_id>/add-image', methods=['POST'])
@jwt_required()
def add_image(package_id):

    if not get_jwt().get('is_admin', False):
        return jsonify({'message': 'Admin access required'}), 403
    
    travel_data = request.get_json()

    imageURL = travel_data.get('imageURL', faker.image_url())
    
    package = Package.query.filter_by(packageId=package_id).first()

    if not package:
        return jsonify({'message': 'Travel package does not exist'}), 400
    
    new_image = PackageImage(imageURL=imageURL, imagePackageId=package_id)

    db.session.add(new_image)
    db.session.commit()

    return jsonify({'message': 'Travel image added successfully'}), 201



@package_bp.route('/<package_id>/delete-image/<image_id>', methods=['DELETE'])
@jwt_required()
def delete_image(package_id, image_id):

    if not get_jwt().get('is_admin', False):
        return jsonify({'message': 'Admin access required'}), 403

    package_image = PackageImage.query.filter_by(imagePackageId=package_id, imageId=image_id).first()

    if not package_image:
        return jsonify({'message': 'Travel-image / package does not exists.'}), 400
    
    db.session.delete(package_image)
    db.session.commit()

    return jsonify({'message': 'Travel image deleted successfully'}), 200


@package_bp.route('/search', methods=['GET'])
@jwt_required()
def search_packages():

    search_term = request.args.get('term').lower()

    print(search_term)

    if not search_term:
        return jsonify({'message': 'Search term not provided'}), 400
    
    packages = Package.query.filter(
                    Package.packageName.contains(search_term) | Package.packageDescription.contains(search_term)
                    ).all()
    return jsonify([package.serialize() for package in packages])