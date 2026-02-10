from datetime import date, timedelta

from .models import Card


def update_card(card: Card,stupidity:int) -> Card:
    """
    Studipity: higher mean more stupid
    """
    if stupidity < 3:
        if card.repetitions == 0:
            card.interval = 1.0
        elif card.repetitions == 1:
            card.interval = 3.0
        else:
            card.interval = card.interval * card.easiness_factor
        card.repetitions += 1
        card.easiness_factor = card.easiness_factor + (0.1 - stupidity * (0.08 + stupidity*0.02))
        if card.easiness_factor < 1.3:
            card.easiness_factor = 1.3
    else:
        card.repetitions=0
        card.interval=1.0
    card.last_review = date.today()
    card.next_review = date.today() + timedelta(days=int(card.interval))
    return card
