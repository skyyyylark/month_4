from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Sum


class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    date = models.DateField()
    age_restriction = models.CharField(max_length=4)
    genres = models.ManyToManyField(Genre, null=True, blank=True)

    def __str__(self):
        return self.name

    def rating(self):
        count_reviews = (self.reviews.count())
        sum = self.reviews.agggregate(Sum('rate'))['rate__sum']
        try:
            return sum / count_reviews
        except:
            return 0

class Category(models.Model):
    name = models.CharField(max_length=100)


class Tag(Category):
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=7)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags')



class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rate = models.IntegerField(default=5)

    def __str__(self):
        return self.movie.name

class PrReviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    review = models.TextField()
    rate = models.IntegerField(default=5)

    def __str__(self):
        return self.review


class PrTag(models.Model):
    is_active = models.BooleanField(default=False)
    tag = models.CharField(max_length=50)
    def __str__(self):
        return self.tag

class ConfirmCode(models.Model):
    code = models.CharField(max_length=100)
    valid_until = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
