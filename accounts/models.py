from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to="profile/%Y/%m", height_field='height_field', width_field='width_field', blank=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    country = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)   
    
    def __str__(self):
        return "Profile for {}".format(self.user.username)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile, sender=User)