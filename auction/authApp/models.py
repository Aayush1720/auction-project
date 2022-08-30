from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User# Create your models here.

# custom user

class userProfile(models.Model):
    email           = models.EmailField(verbose_name="email", max_length=60, unique=True)
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    First_Name      = models.CharField(max_length=100)
    Last_Name       = models.CharField(max_length=100)
    Contact_Number  = models.CharField(max_length=100,null=True)
    balance         = models.FloatField(default=0.00,null=True)

    def __str__(self):
        return self.First_Name

   
