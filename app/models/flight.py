from .base_model import BaseModel, db
from datetime import datetime
from app.utils.enums import FlightStatus


class Flight(BaseModel):
    __tablename__ = 'flights'

    flight_code = db.Column(db.String(125), nullable=False)
    status = db.Column(db.Enum(FlightStatus), nullable=False)
    from_location = db.Column(db.String(125), nullable=False)
    to_location = db.Column(db.String(125), nullable=False)
    departure_time = db.Column(db.DateTime(), nullable=False)
    arrival_time = db.Column(db.DateTime(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    no_of_seats = db.Column(db.Integer(), nullable=False)
    departure_date = db.Column(db.Date(), nullable=False)
    flight_seats = db.relationship('FlightSeat', lazy=True)
