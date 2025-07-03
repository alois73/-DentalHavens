from django.db import models

# Create your models here.
class Promoter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, default='password')
    phone = models.CharField(max_length=15)
    country = models.TextField()
    exp = models.IntegerField(default=0)
    tier = models.CharField(max_length=50, choices=[('Starter', 'Starter'), ('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold'), ('VIP Partner', 'VIP Partner')], default='Tier 1')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    CASHOUT_STATUS_CHOICES = [
    ('None', 'No Request'),            # Default when no cashout has been requested
    ('Requested', 'Requested'),        # When the user clicks the cashout button
    ('Processing', 'Processing'),      # When an admin begins handling the request
    ('Approved', 'Approved'),          # When the request is approved and paid
    ('Rejected', 'Rejected'),          # If the admin rejects the request
    ('Paid', 'Paid'),                  # Optional: to explicitly track payout confirmation
    ]
    cashout_status = models.CharField(max_length=50, choices=CASHOUT_STATUS_CHOICES, default='None')

    def __str__(self):
        return f"({self.name} / {self.username}) ({self.email}) - {self.phone}, {self.country}, Exp: {self.exp}, Tier: {self.tier}, Balance: {self.balance})"

class Code(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    ref_code = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(Promoter, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ref_code} - {self.user.name}"
