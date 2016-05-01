from django.db import models


class RealEstate(models.Model):
    street = models.CharField(max_length=256)
    price = models.IntegerField()
    postDate = models.DateTimeField()
    rooms = models.IntegerField()
    area = models.FloatField()
    zip = models.CharField(max_length=3)
    type = models.CharField(max_length=40)
    description = models.TextField()
    siteID = models.CharField(max_length=12)
