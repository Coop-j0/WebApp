from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from register.models import CustomUser
from payapp.models import UserProfile
from .models import CustomUser

for user in CustomUser.objects.all():
    UserProfile.objects.get_or_create(user=user)

class CustomUserCreationForm(UserCreationForm):
    currency = forms.ChoiceField(choices=UserProfile.CURRENCY_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']



    def save(self, commit=True):
        user = super().save(commit)
        user.userprofile.currency = self.cleaned_data['currency']
        user.userprofile.save()
        return user



class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']