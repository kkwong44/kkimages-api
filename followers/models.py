'''
Followers app
'''
from django.db import models
from django.contrib.auth.models import User


class Follower(models.Model):
    """
    Follower model, related to user.
    """
    owner = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(
        User, related_name='followed', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        '''
        Order by creation date in decending order
        '''
        ordering = ['-created_at']
        unique_together = ['owner', 'followed']

    def __str__(self):
        '''
        Returning by owner's follower
        '''
        return f'{self.owner} {self.followed}'
