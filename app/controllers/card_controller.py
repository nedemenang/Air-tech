'''
    A controller module for card-controller
'''
from datetime import datetime
from app.controllers.base_controller import BaseController
from app.repositories.card_detail_repo import CardDetailRepo


class CardDetailController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.card_detail_repo = CardDetailRepo()

    def list_card_details(self):
        card_details = self.card_detail_repo.filter_by(**{'is_deleted': 'false'})
        card_details_list = [card_detail.serialize() for card_detail in card_details.items]
        return self.handle_response('OK', payload={'cardDetails': card_details_list, 'meta': self.pagination_meta(card_details)})

    def get_card_details(self, card_details_id):
        card_detail = self.card_detail_repo.get(card_details_id)
        if card_detail:
            card_detail = card_detail.serialize()
            return self.handle_response('OK', payload={'cardDetail': card_detail})
        else:
            return self.handle_response('Bad Request - Invalid or missing card_details_id', status_code=400)

    def create_card_details(self):
        card_number, expiry_month, expiry_year, security_number, user_id = self.request_params("cardNumber", "expiryMonth", "expiryYear", "securityNumber", "userId")
        card_detail = self.card_detail_repo.create_card_detail(card_number, expiry_month, expiry_year, security_number, user_id)
        return self.handle_response('OK', payload={'cardDetail': card_detail.serialize()})

    def update_card_details(self, card_details_id):
        card_number, expiry_month, expiry_year, security_number = self.request_params("cardNumber", "expiryMonth", "expiryYear", "securityNumber")

        card_detail = self.card_detail_repo.get(card_details_id)

        if card_detail:
            updates = {}
            if card_number:
                updates['card_number'] = card_number
            if expiry_month:
                updates['expiry_month'] = expiry_month
            if expiry_year:
                updates['expiry_year'] = expiry_year
            if security_number:
                updates['securiy_number'] = security_number

            self.card_detail_repo.update(card_detail, **updates)
            return self.handle_response('OK', payload={'cardDetail': card_detail.serialize()})
        return self.handle_response('Invalid or incorrect card_detail_id provided', status_code=400)

    def delete_card_detail(self, card_detail_id):
        card_detail = self.card_detail_repo.get(card_detail_id)
        updates = {}

        if card_detail:
            updates['is_deleted'] = True

            self.card_detail_repo.update(card_detail, **updates)
            return self.handle_response('OK', payload={'status': 'success'})
        return self.handle_response('Invalid or incorrect card_detail_id provided', status_code=400)


