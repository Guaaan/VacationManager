from django.db import models
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator

class VacationRequest(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vacation_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    days_requested = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(Decimal('0.1'))])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    ms_event_id = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} | {self.start_date} -> {self.end_date} ({self.days_requested})"
