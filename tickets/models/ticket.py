from django.db import models
from django.contrib.auth.models import User
from tickets.models import Station


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    from_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="from_tickets"
    )
    to_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="to_tickets"
    )
    date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} | {self.from_station} → {self.to_station}"
