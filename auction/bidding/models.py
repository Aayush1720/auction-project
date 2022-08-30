from django.db import models
from authApp.models import *
from datetime import datetime


# Create your models here.
class product(models.Model):
    pid = models.IntegerField(null=False, unique=True, primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True)
    basePrice = models.FloatField(null=False)
    curPrice = models.FloatField(null=False)
    image1 = models.ImageField(null=True, blank=True,upload_to='images')
    description = models.TextField(null=True,blank=True)
    age = models.IntegerField(null=True)
    deadline = models.DateTimeField()
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.image1.url
        except:
            url = ''
        
        return url
    @property
    def isComplete(self):
        if self.deadline <= datetime.now():
            self.complete = True
        
        return self.complete

class bid(models.Model):
    bidder = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    prevPrice = models.FloatField(null=True)
    curPrice = models.FloatField()
    active = models.BooleanField(default=True)


    
