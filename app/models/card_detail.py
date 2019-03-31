from .base_model import BaseModel, db


class CardDetail(BaseModel):
    __tablename__ = "card_details"

    card_number = db.Column(db.String(120), nullable=False)
    expiry_month = db.Column(db.Integer(), nullable=False)
    expiry_year = db.Column(db.Integer(), nullable=False)
    securiy_number = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    user = db.relationship('User', lazy=False)
