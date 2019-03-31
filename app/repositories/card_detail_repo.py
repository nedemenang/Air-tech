from app.repositories.base_repo import BaseRepo
from app.models.card_detail import CardDetail
from datetime import datetime


class CardDetailRepo(BaseRepo):

    def __init__(self):
        BaseRepo.__init__(self, CardDetail)

    def create_card_detail(self, card_number, expiry_month, expiry_year, security_number, user_id):
        print('I am here')
        card_Detail = CardDetail(card_number=card_number, expiry_month=expiry_month, expiry_year=expiry_year, securiy_number=security_number, user_id=user_id)

        card_Detail.save()
        return card_Detail
