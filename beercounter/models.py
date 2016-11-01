from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


class User(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'User ' + self.name


class Drink(models.Model):
    name = models.CharField(max_length=50)
    crate_size = models.IntegerField(default=24)

    def __str__(self):
        return 'Drink ' + self.name


class Consumption(models.Model):
    user = models.ForeignKey(User)
    drink = models.ForeignKey(Drink)
    datetime = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return "%d at %s" % (self.count, self.datetime.isoformat())


# receives signal when a new user is created to add a token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)