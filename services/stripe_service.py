import stripe
from django.conf import settings
from users.models import Payment  # Импортируем из users, не из materials

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(course, user, request):
    """Создает Stripe Checkout Session для оплаты курса"""

    # Создаем продукт
    product = stripe.Product.create(
        name=course.title,
    )

    # Создаем цену
    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(course.price * 100),
        currency="usd",
    )

    # Создаем сессию оплаты
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url='http://127.0.0.1:8000/payment/success/',
        cancel_url='http://127.0.0.1:8000/payment/cancel/',
        customer_email=user.email,
    )

    # Сохраняем платеж в модели Payment
    Payment.objects.create(
        user=user,
        course=course,
        amount=course.price,
        payment_method="stripe",
        stripe_checkout_session_id=checkout_session.id,
    )

    return checkout_session
