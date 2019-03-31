from .base_model import BaseModel, db
from app.models.flight import Flight


class FlightSeat(BaseModel):
    __tablename__ = "flight_seats"

    flight_id = db.Column(db.Integer(), db.ForeignKey('flights.id'), nullable=False)
    seat_number = db.Column(db.Text(), nullable=False)
    is_available = db.Column(db.Boolean(), nullable=False)
    flight = db.relationship('Flight', lazy=False)
