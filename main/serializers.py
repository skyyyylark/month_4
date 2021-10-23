from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main.models import Movie, Product, Review, Category, Tag, Genre, PrReviews, PrTag


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id rate text'.split()

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
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

class PrReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrReviews
        fields = ['product', 'review', 'rate']



class PrTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrTag
        fields = '__all__'

class CreateMovieValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=100)
    duration = serializers.IntegerField()
    datetime = serializers.DateField()
    age_restriction = serializers.CharField(min_length=2, max_length=3)
    genres = serializers.ListField(child=serializers.IntegerField(), required=True)

    def validate_name(self, name):
        movies = Movie.objects.filter(name=name)
        if movies.count() > 0:
            raise ValidationError("Такой фильм уже существует")
        return name

    def validate_age(self, age):
        if age [-1] != '+':
            raise ValidationError('Последний символ должен быть "+"!')
        try:
            int(age[0:-1])
        except:
            raise ValidationError('До "+" должно быть число!')

class CreateProductValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    price = serializers.CharField(max_length=7)
    category = serializers.CharField(max_length=100)
    tags = serializers.IntegerField()

    def validate_name(self, name):
        products = Product.objects.filter(name=name)
        if products.count() > 0:
            raise ValidationError("Такой продукт уже добавлен")
        return name

    def validate_tag_serializer(self, tags):
        products = Product.objects.filter(tags=tags)
        if tags.count() > 0:
            raise ValidationError('Данный продукт уже существует')
        return tags

        


