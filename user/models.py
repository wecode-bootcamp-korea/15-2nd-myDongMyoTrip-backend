from django.db import models

class SocialPlatform(models.Model):
    platform = models.CharField(max_length=45)

    class Meta:
        db_table = 'social_platforms'

class User(models.Model):
    name                = models.CharField(max_length=45)
    email               = models.EmailField(max_length=100, unique=True)
    password            = models.CharField(max_length=250)
    is_location_agreed  = models.BooleanField(default=False)
    is_promotion_agreed = models.BooleanField(default=False)
    social_platform     = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, null=True)
    social_id           = models.CharField(max_length=200)
    is_active           = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class RecentView(models.Model):
    flight    = models.ForeignKey('flight.Flight', on_delete=models.CASCADE)
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recent_views'
