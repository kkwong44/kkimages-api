'''
Comments app
'''
from django.db import models
from django.contrib.auth.models import User
from albums.models import Album


class Comment(models.Model):
    """
    Comment model, related to owner's album.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)

    class Meta:
        '''
        Order by creation date in decending order
        '''
        ordering = ['-created_at']

    def __str__(self):
        '''
        Returning by comment's content
        '''
        return f"{self.content}"
