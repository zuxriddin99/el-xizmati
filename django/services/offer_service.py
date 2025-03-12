from rest_framework import exceptions

from apps.ads.models import Offer, AD, OfferStatus


class OfferService:

    @staticmethod
    def send_offer(ad_id: int, user_id: int):
        try:
            Offer.objects.get(ad_id=ad_id, user_id=user_id)
            raise exceptions.ParseError(detail='You already send offer for the ad', code="ALREADY_SEND_OFFER")
        except Offer.DoesNotExist:
            offer = Offer.objects.create(ad_id=ad_id, user_id=user_id)
            return offer

    def accept_offer(self, offer_id: int, user_id: int):
        offer = self.get_offer_or_raise(offer_id=offer_id)
        if user_id != offer.ad.owner_id:
            raise exceptions.ParseError(detail='Only owner of ad can accept the offer', code="HAS_NOT_PERMISSION")
        offer.status = OfferStatus.PROCESSING
        offer.save()
        # todo: need to add push notificator for worker

    def cancel_offer(self, offer_id: int, user_id: int):
        offer = self.get_offer_or_raise(offer_id=offer_id)
        if user_id == offer.user_id:
            pass
            # todo: need to send push  notification about
        elif user_id == offer.ad.owner_id:
            # todo: need to send push  notification about
            pass
        else:
            raise exceptions.ParseError(detail='Only worker or ad owner can cancel the offer', code="HAS_NOT_PERMISSION")

        offer.status = OfferStatus.CANCELED
        offer.save()

    def complete_offer(self, offer_id: int, user_id: int):
        offer = self.get_offer_or_raise(offer_id=offer_id)
        if user_id == offer.user_id:
            offer.worker_was_completed = True
            offer.save()
            # todo: need to send push  notification about
        elif user_id == offer.ad.owner_id:
            offer.owner_was_confirmed = True
            offer.save()
            # todo: need to send push  notification about
        else:
            raise exceptions.ParseError(detail='Only worker or ad owner can cancel the offer',
                                        code="HAS_NOT_PERMISSION")
        if offer.worker_was_completed and offer.owner_was_confirmed:
            offer.status = OfferStatus.COMPLETED
            offer.save()

    @staticmethod
    def get_offer_or_raise(offer_id: int):
        try:
            return Offer.objects.get(id=offer_id)
        except Offer.DoesNotExist:
            raise exceptions.NotFound(detail='Entered offer not found.', code="NOT_FOUND")

    @staticmethod
    def get_worker_offers(user_id: int):
        return Offer.objects.filter(user_id=user_id)

    @staticmethod
    def get_employer_offers(user_id: int):
        return Offer.objects.filter(ad__owner_id=user_id)
