"""
Import libraries for User Profile App
"""
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    '''
    Setting up Profile model
    '''
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='kkimages/', default='../default_profile_omrhyn'
    )

    class Meta:
        '''
        Order by creation date in decending order
        '''
        ordering = ['-created_at']

    def __str__(self):
        '''
        Returning owner's proflie information
        '''
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    '''
    Connect to post_save signal and creating user profile
    '''
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
