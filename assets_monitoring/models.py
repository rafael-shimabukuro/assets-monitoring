from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    objects = models.Manager()
    ticker = models.CharField(max_length=10, unique=True, null=False)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    update_interval_minutes = models.PositiveIntegerField(default=10, null=False)
    last_update = models.DateTimeField(null=True)
    next_update = models.DateTimeField(null=True)
    users = models.ManyToManyField(User, through='AssetOwnership')

    def __str__(self):
        return self.ticker


class AssetOwnership(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=False)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    update_interval_minutes = models.PositiveIntegerField(default=10, null=False)
    notified_time = models.DateTimeField(null=True)
