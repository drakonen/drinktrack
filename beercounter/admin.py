from django.contrib import admin

from .models import User, Consumption, Drink

admin.site.register(User)
admin.site.register(Consumption)
admin.site.register(Drink)
