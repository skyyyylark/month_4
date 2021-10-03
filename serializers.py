from rest_framework import serializers
from main.models import Movie, Product, Review, Category, Tag, Genre

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id rate text'.split()

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    filtered = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'name', 'genres', 'duration', 'reviews', 'rating']
    def get_filtered(self, movie):
        reviews = Review.objects.filter(movie=movie).exclude(text__contains='ниггер')
        return ReviewSerializer(reviews, many=True).data

class ProductsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'