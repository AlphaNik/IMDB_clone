from django.db import models
from django.core import validators
from django.contrib.auth.models import User


class StreamPlatform(models.Model):
    name = models.CharField(max_length=20)
    about = models.CharField(max_length=200)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0,null=True)
    number_of_ratings = models.IntegerField(default=0,null=True)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE,related_name='watchlist')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    review_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    rating = models.PositiveIntegerField(validators=[validators.MinValueValidator(1),
                                                     validators.MaxValueValidator(5)])
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE,related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.rating} | {self.watchlist.title}'