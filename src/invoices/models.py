from django.db import models
from profiles.models import Profile
from receivers.models import Receiver


class Tag(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Invoice(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE) 
    number = models.CharField(max_length=150)
    completion_date = models.DateField()
    issue_date = models.DateField()
    payment_day = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    # if closed - hide add positions and unable adding new once
    closed = models.BooleanField(default=False)
    # we add tag only for educational purposes
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return f'invoice number: {self.number}, pk: {self.pk}'
    
    @property
    def tags(self):
        return self.tags.all()
    
    @property
    def positions(self):
        return self.position_set.all()
    
    @property
    def total_amount(self):
        total = 0
        qs = self.positions
        for pos in qs:
            total += pos.amount
        return total
