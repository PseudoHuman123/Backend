from flask import Blueprint, jsonify, request
import faker
from flask_jwt_extended import get_jwt, jwt_required
from models import Package, Booking
from db import db
import datetime

booking_bp = Blueprint('booking', __name__)
faker = faker.Faker()

@booking_bp.route('/show', methods=['GET'])
@jwt_required()
def get_bookings():
    all_bookings = Booking.query.all()
    return jsonify([booking.serialize() for booking in all_bookings])

@booking_bp.route('/show/<booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    booking = Booking.query.filter_by(bookingId=booking_id).first()
    if not booking:
        return jsonify({'message': 'Booking does not exist'}), 404
    return jsonify(booking.serialize())


@booking_bp.route('/add', methods=['POST'])
@jwt_required()
def add_booking():
    booking_data = request.get_json()

    bookingUserId = booking_data.get('bookingUserId')
    bookingPackageId = booking_data.get('bookingPackageId')

    if not bookingUserId or not bookingPackageId:
        return jsonify({'message': 'Booking user or package id not provided'}), 400

    bookingStartDate = booking_data.get('bookingStartDate', faker.date())

    bookingStartDate = datetime.datetime.strptime(bookingStartDate, '%Y-%m-%d').date()
    bookingEndDate = bookingStartDate + datetime.timedelta(days=Package.query.filter_by(packageId=bookingPackageId).first().packageDuration)


    bookingSlots = booking_data.get('bookingSlots', faker.random_int(min=1, max=10))

    if bookingSlots > Package.query.filter_by(packageId=bookingPackageId).first().packageSlots:
        return jsonify({'message': 'Booking slots greater than available slots'}), 400

    bookingCost = bookingSlots * Package.query.filter_by(packageId=bookingPackageId).first().packageCost

    new_booking = Booking(
        bookingUserId = bookingUserId,
        bookingPackageId = bookingPackageId,
        bookingStartDate = bookingStartDate,
        bookingEndDate = bookingEndDate,
        bookingSlots = bookingSlots,
        bookingCost = bookingCost
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({
        "message": "Booking added successfully", 
        "booking": new_booking.serialize()
    }), 201

@booking_bp.route('/package/<package_id>', methods=['GET'])
@jwt_required()
def get_bookings_by_package(package_id):

    if not get_jwt().get('is_admin', False):
        return jsonify({'message': 'Admin access required'}), 403
    
    package_bookings = Booking.query.filter_by(bookingPackageId=package_id).all()
    return jsonify([booking.serialize_without_package() for booking in package_bookings])

@booking_bp.route('/user/<user_id>', methods=['GET'])
@jwt_required()
def get_bookings_by_user(user_id):
    user_bookings = Booking.query.filter_by(bookingUserId=user_id).all()
    return jsonify([booking.serialize_without_user() for booking in user_bookings])