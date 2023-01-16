from django.db import models
from datetime import datetime



class Receiver(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    website = models.URLField(blank=True)
    created = models.DateTimeField(default=datetime.now)
    
    logo = models.ImageField(default="images/no_photo.png")
    
    def __str__(self):
        return str(self.name)
