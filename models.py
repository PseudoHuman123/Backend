from db import db
import faker
import uuid 
from datetime import datetime

def get_uuid(): return str(uuid.uuid4())

class Package(db.Model):
    __tablename__ = 'packages'

    packageId = db.Column(db.String, primary_key=True, default=get_uuid)
    packageName = db.Column(db.String, nullable=False)
    packageDescription = db.Column(db.String, nullable=False)
    packageDuration = db.Column(db.Integer, nullable=False)
    packageCost = db.Column(db.Float, nullable=False)
    packageSlots = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f'<TravelPackage {self.packageName}>'
    
    def serialize(self):
        return {
            'packageId': self.packageId,
            'packageName': self.packageName,
            'packageDescription': self.packageDescription,
            'packageDuration': self.packageDuration,
            'packageCost': self.packageCost,
            'packageSlots': self.packageSlots,
            'packageImageURL': [image.imageURL for image in PackageImage.query.filter_by(imagePackageId=self.packageId).all()]
        }
    
class PackageImage(db.Model):
    __tablename__ = 'package_images'

    imageId = db.Column(db.String, primary_key=True, default=get_uuid)
    imageURL = db.Column(db.String, nullable=False)
    imagePackageId = db.Column(db.String, db.ForeignKey('packages.packageId'), nullable=False)

    def __repr__(self):
        return f'<TravelImage {self.imageURL}>'
    
class User(db.Model):
    __tablename__ = 'users'

    userId = db.Column(db.String, primary_key=True, default=get_uuid)
    userEmail = db.Column(db.String, nullable=False, unique=True)
    userName = db.Column(db.String, nullable=False)
    userPassword = db.Column(db.String, nullable=False)


    def __repr__(self):
        return f'<User {self.userName}>'
    
    def serialize(self):
        return {
            'userId': self.userId,
            'userName': self.userName,
            'userEmail': self.userEmail,
        }
    
class Booking(db.Model):
    __tablename__ = 'bookings'

    bookingId = db.Column(db.String, primary_key=True, default=get_uuid)
    bookingUserId = db.Column(db.String, db.ForeignKey('users.userId'), nullable=False)
    bookingPackageId = db.Column(db.String, db.ForeignKey('packages.packageId'), nullable=False)
    bookingDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bookingStartDate = db.Column(db.DateTime, nullable=False)
    bookingEndDate = db.Column(db.DateTime, nullable=False)
    bookingSlots = db.Column(db.Integer, nullable=False)
    bookingCost = db.Column(db.Float, nullable=False)

    
    def __repr__(self):
        return f'<Booking {self.bookingId}>'
    
    def serialize(self):
        return {
            'bookingId': self.bookingId,
            'bookingUserDetails': User.query.filter_by(userId=self.bookingUserId).first().serialize(),
            'bookingPackageId': Package.query.filter_by(packageId=self.bookingPackageId).first().serialize(),
            'bookingDate': self.bookingDate,
            'bookingStartDate': self.bookingStartDate,
            'bookingEndDate': self.bookingEndDate,
            'bookingSlots': self.bookingSlots,
            'bookingCost': self.bookingCost,
        }
    
    def serialize_without_package(self):
        return {
            'bookingId': self.bookingId,
            'bookingUserDetails': User.query.filter_by(userId=self.bookingUserId).first().serialize(),
            'bookingDate': self.bookingDate,
            'bookingStartDate': self.bookingStartDate,
            'bookingEndDate': self.bookingEndDate,
            'bookingSlots': self.bookingSlots,
            'bookingCost': self.bookingCost,
        }

    def serialize_without_user(self):
        return {
            'bookingId': self.bookingId,
            'bookingPackageDetails': Package.query.filter_by(packageId=self.bookingPackageId).first().serialize(),
            'bookingDate': self.bookingDate,
            'bookingStartDate': self.bookingStartDate,
            'bookingEndDate': self.bookingEndDate,
            'bookingSlots': self.bookingSlots,
            'bookingCost': self.bookingCost,
        }
