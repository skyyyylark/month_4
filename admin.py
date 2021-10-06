from django.contrib import admin

# Register your models here.
from .models import Movie, Product, Category, Tag, Review, Genre, PrReviews, PrTag

admin.site.register(Movie)

admin.site.register(Review)

admin.site.register(Product)

admin.site.register(Tag)

admin.site.register(Category)

admin.site.register(Genre)

admin.site.register(PrReviews)

admin.site.register(PrTag)
