from django import forms
from register.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class PaymentForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label="Recipient")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")

class PaymentRequestForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label="Recipient")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")
    description = forms.CharField(max_length=255, label="Description", required=False)

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']