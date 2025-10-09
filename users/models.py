from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

class User(AbstractUser):
    vacation_days = models.DecimalField(max_digits=6, decimal_places=1, default=Decimal('15.0'))
    ms_graph_id = models.CharField(max_length=200, blank=True, null=True)
