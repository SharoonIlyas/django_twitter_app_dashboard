from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Tweet(models.Model):
    text = models.CharField(max_length = 300 , default = '')
    datetime= models.DateTimeField(default = timezone.now)
    user =  models.ForeignKey(User, on_delete=models.CASCADE , null = True) 
    
    def __str__(self):
        return self.text  
    
