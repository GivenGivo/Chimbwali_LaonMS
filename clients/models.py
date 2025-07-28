from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class Client(models.Model):
    full_name = models.CharField(max_length=100)
    nrc = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    passport_photo = models.ImageField(upload_to='photos/')
    signature = models.ImageField(upload_to='signatures/')

    business_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    relationship_with_witness = models.CharField(max_length=255, blank=True, null=True)

    # Surety Info
    surety_name = models.CharField(max_length=100)
    surety_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    surety_make = models.CharField(max_length=255, blank=True, null=True)

    # Witness Info
    witness_name = models.CharField(max_length=100)
    witness_nrc = models.CharField(max_length=20)
    witness_phone = models.CharField(max_length=20)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Approval status
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.nrc}"



from django.db import models
from django.conf import settings
from decimal import Decimal
from datetime import timedelta

from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from django.db import models
from django.conf import settings

class Loan(models.Model):
    EXEMPT_DAY_CHOICES = [
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    ]

    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='loans')
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    repayment_days_created = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('37.8'))
    exempt_day = models.CharField(max_length=10, choices=EXEMPT_DAY_CHOICES, default='SUNDAY')

    def __str__(self):
        return f"{self.client.full_name} - Loan #{self.id} - ZMW {self.amount}"

    @property
    def total_with_interest(self):
        total = self.amount + (self.amount * self.interest_rate / Decimal('100'))
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def repayment_day_count(self):
        return 26  # Per business rule (excluding exempt days)

    @property
    def daily_payment(self):
        daily = self.total_with_interest / Decimal(self.repayment_day_count)
        return daily.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def total_paid(self):
        """
        Sum of actual submitted `amount_paid` on paid days.
        """
        return self.repayment_days.filter(is_paid=True).aggregate(
            total=models.Sum('amount_paid')
        )['total'] or Decimal('0.00')

    def balance(self):
        """
        Total remaining balance = Total with interest - Actual total paid.
        """
        return max(self.total_with_interest - self.total_paid(), Decimal('0.00'))

    def is_settled(self):
        return self.balance() <= Decimal('0.00')

    @property
    def due_date(self):
        """
        Last repayment date (based on repayment_days).
        """
        last_day = self.repayment_days.order_by('-day_number').first()
        return last_day.date if last_day else None




class LoanRepaymentDay(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE, related_name='repayment_days')
    date = models.DateField()
    day_number = models.PositiveIntegerField()  # 1 to 26

    is_paid = models.BooleanField(default=False)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_repayments'
    )
    marked_at = models.DateTimeField(null=True, blank=True)

    corrected_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='edited_repayments'
    )
    edited_at = models.DateTimeField(null=True, blank=True)
    edit_note = models.TextField(blank=True, null=True)

    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text="Actual amount paid on this day"
    )

    balance_carried_forward = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text="Shortfall forwarded to next unpaid day"
    )

    class Meta:
        unique_together = ('loan', 'day_number')
        ordering = ['day_number']

    def __str__(self):
        return f"Day {self.day_number} - {self.date} - {'PAID' if self.is_paid else 'UNPAID'}"

    @property
    def amount_due(self):
        return self.corrected_amount if self.corrected_amount is not None else self.loan.daily_payment


from django.db import models
from django.conf import settings

class DailyReport(models.Model):
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    date = models.DateField()  # Explicit report date
    total_expected = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_collected = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_payments = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    accumulative_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    clients_owing = models.PositiveIntegerField(default=0)
    
    optional_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.submitted_by.username} - {self.date}"


from django.db import models
from django.conf import settings

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


from django.db import models

class TermsAndConditions(models.Model):
    title = models.CharField(max_length=255, default="Terms and Conditions")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title