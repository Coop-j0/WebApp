from django.contrib.auth import get_user_model
from django.db import models


class Transaction(models.Model):
    sender = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='sent_transactions', null=True, blank=True)
    recipient = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='received_transactions', null=True, blank=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=[('payment', 'Payment'), ('request', 'Request')])
    is_request_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type.title()} from {self.sender.user.username} to {self.recipient.user.username} - £{self.amount}"

CustomUser = get_user_model()

class UserProfile(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),

    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='userprofile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=750)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    def __str__(self):
        return f"{self.user.username}'s profile"