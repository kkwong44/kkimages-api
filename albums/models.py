from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    """
    Album model, related to 'owner', i.e. a User instance.
    Default cover image set so that we can always reference image.url.
    """
    category_filter_choices = [
        ('wedding', 'Wedding'),
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
        ('baby', 'Baby'),
        ('animals', 'Animals'),
        ('general', 'General'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    cover_image = models.ImageField(
        upload_to='kkimages/', default='../default_post_liudmg', blank=True
    )
    category_filter = models.CharField(
        max_length=32, choices=category_filter_choices, default='general')

    class Meta:
        '''
        Order by creation date in decending order
        '''
        ordering = ['-created_at']

    def __str__(self):
        '''
        Returning by album's id and title
        '''
        return f'{self.id} {self.title}'
