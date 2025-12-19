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
        station_names = set()
        while len(station_names) < 5:
            station_names.add(faker.city())

        for name in station_names:
            Station.objects.create(name=name)

        self.stdout.write(self.style.SUCCESS("Stations created"))

        # ---- Tickets ----
        users = list(User.objects.all())
        stations = list(Station.objects.all())

        print("users =>", users)
        print("stations =>", stations)

        for _ in range(5):
            from_station, to_station = random.sample(stations, 2)
            price = abs(from_station.id - to_station.id) + 100

            Ticket.objects.create(
                user=random.choice(users),
                from_station=from_station,
                to_station=to_station,
                date=faker.date_this_year(),
                price=price,
            )

        self.stdout.write(self.style.SUCCESS("Tickets created"))
