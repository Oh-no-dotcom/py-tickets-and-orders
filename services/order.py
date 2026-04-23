from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict[str, int]],
        username: str,
        date: str = None,
) -> None:
    username_ = get_user_model().objects.get(username=username)

    order_kwargs = {"user": username_}
    if date is not None:
        order_kwargs["created_at"] = datetime.strptime(date, "%Y-%m-%d %H:%M")
    order = Order.objects.create(**order_kwargs)

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )


def get_orders(
        username: str = None
) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
