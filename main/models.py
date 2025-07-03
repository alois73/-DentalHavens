from django.db import models
from affiliate_program.models import Code
from decimal import Decimal

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('Imaging', 'Imaging'),
        ('Surgery', 'Surgery'),
        ('Orthopedist', 'Orthopedist'),
        ('Prophylaxis', 'Prophylaxis'),
        ('Therapy', 'Therapy')
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, default='no category')

    def __str__(self):
        return self.name
    
class Tour(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    phone_number = models.CharField(max_length=15)
    tour_option = models.CharField(max_length=100, choices=[('City Tour', 'City Tour'), ('Historical Tour', 'Historical Tour'), ('Cultural Tour', 'Cultural Tour'), ('Adventure / Hiking Tour', 'Adventure / Hiking Tour'), ('Experiences / Ural Tour', 'Experiences / Ural Tour'), ('Customized Tour', 'Customized Tour'), ('', 'No Tour')], blank=True, default='')
    custom_request = models.TextField(max_length=500, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ref_code = models.ForeignKey(Code, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=100, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Pending')
    rewarded = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    def reward_promoter(self):
        print(f"🔁 reward_promoter called for {self.email}")
        if self.ref_code and self.status == 'Confirmed' and not self.rewarded:
            try:
                promoter = self.ref_code.user
                print(f"🎯 Promoter: {promoter.username} (Exp: {promoter.exp}, Tier: {promoter.tier}, Balance: {promoter.balance})")

                if promoter.tier == 'VIP Partner':
                    bal_add = Decimal('120.00')
                    print(f"✅ VIP Partner: Adding ${bal_add} to promoter, new balance: {promoter.balance}")
                else:
                    if promoter.exp >= 30:
                        promoter.tier = 'Gold'
                        bal_add = Decimal('70.00')
                    elif promoter.exp >= 15:
                        promoter.tier = 'Silver'
                        bal_add = Decimal('50.00')
                    elif promoter.exp >= 5:
                        promoter.tier = 'Bronze'
                        bal_add = Decimal('35.00')
                    else:
                        promoter.tier = 'Starter'
                        bal_add = Decimal('25.00')

                promoter.balance += bal_add
                print(f"✅ Adding ${bal_add} to promoter, new balance: {promoter.balance}")
                promoter.save(update_fields=['exp', 'balance', 'tier'])

                self.rewarded = True
                self.save(update_fields=['rewarded'])

            except Exception as e:
                print("❌ Error rewarding promoter:", e)
