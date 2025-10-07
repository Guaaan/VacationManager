from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

class User(AbstractUser):
    # saldo de días (ej: 15.0)
    vacation_days = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal('15.0'))
    # reservado para la integración con MS Graph más adelante
    ms_graph_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.username