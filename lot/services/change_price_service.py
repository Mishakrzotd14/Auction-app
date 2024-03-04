from auction.tasks import send_price_change_email_task
from lot.models import Offer


def send_email_about_change_price(lot, current_user, current_price):
    offer = Offer.objects.filter(lot=lot.pk)
    if offer.exists():
        user_of_offer = offer.latest('date_creation').user
        user_email = user_of_offer.email
        if user_of_offer is not None and user_email != '':
            if user_of_offer != current_user:
                send_price_change_email_task(lot, user_email, current_price)
