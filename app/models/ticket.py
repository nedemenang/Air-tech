from .base_model import BaseModel, db
from app.utils.enums import TicketStatus
from app.models.flight_seats import FlightSeat


class Ticket(BaseModel):
    __tablename__ = "tickets"

    flight_seat_id = db.Column(db.Integer(), db.ForeignKey('flight_seats.id'))
    ticket_no = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum(TicketStatus), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    user = db.relationship('User', lazy=False)
    flight_seat = db.relationship('FlightSeat', lazy=False)
