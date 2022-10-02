"""
Import libraries for Contacts App
"""
from django.db import models


class Contact(models.Model):
    '''
    Setting up Contact model
    '''
    depart_id = models.IntegerField(unique=True)
    department = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    town = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)

    class Meta:
        '''
        Order by creation date in decending order
        '''
        ordering = ['depart_id']

    def __str__(self):
        '''
        Returning company information
        '''
        return f"{self.department}"
