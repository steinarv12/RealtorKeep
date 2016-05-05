from django.db import models


class RealEstate(models.Model):
    street = models.CharField(max_length=256)
    price = models.IntegerField(default=-1)
    postDate = models.DateTimeField(blank=True)
    rooms = models.IntegerField(default=-1)
    area = models.FloatField(default=-1)
    zip = models.CharField(max_length=3, default="000")
    type = models.CharField(max_length=40, default="")
    description = models.TextField(default="")
    siteID = models.CharField(max_length=12, default="")
    pictures = models.TextField(null=True)
