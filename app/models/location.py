from .base_model import BaseModel, db


class Location(BaseModel):
    __tablename__ = "location"

    location_code = db.Column(db.String(125), nullable=False)
    location = db.Column(db.String(125), nullable=False)
