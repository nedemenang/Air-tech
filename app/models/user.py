from .base_model import BaseModel, db


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    middle_name = db.Column(db.String(120), nullable=True)
    photo_link = db.Column(db.String(1000), nullable=True)
    email_address = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(750), nullable=False)
    card_details = db.relationship('CardDetail', lazy=True)
    tickets = db.relationship('Ticket', lazy=True)