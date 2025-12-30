import random
from django.core.management.base import BaseCommand
from faker import Faker
from tickets.models import Station, Ticket
from django.contrib.auth.models import User

faker = Faker()


class Command(BaseCommand):
    help = "Seed fake data into Station and Ticket tables"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Seeding started..."))

        # ---- Stations ----
        for _ in range(5):
            name = faker.city()
            Station.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS("Stations created"))

        # ---- Tickets ----
        users_qs = User.objects.only("id")
        users_count = users_qs.count()
        stations_qs = Station.objects.only("id")
        stations_count = stations_qs.count()

        print("users =>", users_qs, users_count)
        print("stations =>", stations_qs, stations_count)

        for _ in range(5):
            from_station = stations_qs[random.randint(0, stations_count - 1)]
            to_station = stations_qs.exclude(id=from_station.id)[
                random.randint(0, stations_count - 2)
            ]
            price = abs(from_station.id - to_station.id) + 100

            Ticket.objects.get_or_create(
                user=users_qs[random.randint(0, users_count - 1)],
                from_station=from_station,
                to_station=to_station,
                date=faker.date_this_year(),
                price=price,
            )

        self.stdout.write(self.style.SUCCESS("Tickets created"))
