from datetime import date, timedelta, time
from .models import TimeSlot


def generate_slots():
    start = date.today()

    for i in range(2, 200):  # next 200 days
        day = start + timedelta(days=i)

        for hour in range(15, 20):  # 3pm–7pm
            for minutes in [0, 30]:
                t = time(hour, minutes).strftime("%H:%M")

                TimeSlot.objects.get_or_create(
                    day=day,
                    time=t
                )