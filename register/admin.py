from django.contrib import admin

from payapp.models import CustomUser, UserProfile

from django.contrib.auth import get_user_model
User = get_user_model()
admin.site.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_currency', 'get_balance', 'date_joined')

    def get_currency(self, obj):
        return obj.userprofile.currency
    get_currency.short_description = 'Currency'

    def get_balance(self, obj):
        return obj.userprofile.balance
    get_balance.short_description = 'Balance'

admin.site.unregister(CustomUser)

admin.site.register(CustomUser, CustomUserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'balance')

admin.site.register(UserProfile, UserProfileAdmin)