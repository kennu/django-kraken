from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Django 1.3 compatibility
if not hasattr(User, 'get_full_name'):
    def get_full_name(self):
        return (u'%s %s' % (self.first_name, self.last_name)).strip()
    User.get_full_name = get_full_name

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    # Add your user account fields here

def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
