from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.


class Content(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    streamPlatform = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    averageRating = models.FloatField(default=0)
    totalNumberOfRatings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    text = models.CharField(max_length=200, null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='reviews')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + '-' + self.content.title


