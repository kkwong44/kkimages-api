'''
Likes app
'''
from django.db import models
from django.contrib.auth.models import User
from albums.models import Album


class Like(models.Model):
    """
    Like model, related to owner's album.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(
        Album, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        '''
        Order by creation date in decending order
        '''
        ordering = ['-created_at']
        unique_together = ['owner', 'album']

    def __str__(self):
        '''
        Returning by owner's album
        '''
        return f"{self.owner} {self.album}"
