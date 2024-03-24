from auction.tasks import send_price_change_email_task
from lot.models import Offer


def get_last_offer(lot):
    offer = Offer.objects.filter(lot=lot.pk)
    if offer.exists():
        return offer.latest('date_creation')
    return None


def send_email_about_change_price(lot, current_user, current_price):
    last_offer = get_last_offer(lot)
    if last_offer:
        user_of_offer = last_offer.user
        user_email = user_of_offer.email
        if user_email:
            if user_of_offer != current_user:
                send_price_change_email_task(lot, user_email, current_price)
