'''
Photos app
'''
from django.db import models
from django.contrib.auth.models import User
from albums.models import Album


class Photo(models.Model):
    """
    Photo model, related to owner's album.
    Default photo image set so that we can always reference image.url.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    photo_image = models.ImageField(
        upload_to='kkimages/', default='../default_post_liudmg', blank=True
    )

    class Meta:
        '''
        Order by creation date in decending order
        '''
        ordering = ['-created_at']

    def __str__(self):
        '''
        Returning by photo's title
        '''
        return f"Album: {self.album}, {self.title}"
