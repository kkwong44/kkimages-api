'''
Albums app
'''
from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    """
    Album model, related to 'owner', i.e. a User instance.
    Default cover image set so that we can always reference image.url.
    """
    category_filter_choices = [
        ('General', 'General'),
        ('Animals', 'Animals'),
        ('Architecture', 'Architecture'),
        ('Baby', 'Baby'),
        ('Commercial', 'Commercial'),
        ('Fashion', 'Fashion'),
        ('Food', 'Food'),
        ('Landscape', 'Landscape'),
        ('Portrait', 'Portrait'),
        ('Sports', 'Sports'),
        ('Travel', 'Travel'),
        ('Wedding', 'Wedding'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    skill_level = models.CharField(max_length=255)
    cover_image = models.ImageField(
        upload_to='kkimages/', default='../default_post_liudmg', blank=True
    )
    category_filter = models.CharField(
        max_length=32, choices=category_filter_choices, default='General')

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
