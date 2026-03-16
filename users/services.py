import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_price(amount):
    """Создает цену в страйпе."""
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": "Оплата курса"},
    )


def create_stripe_session(price_id):
    """Создает сессию оплаты."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.url, session.id
