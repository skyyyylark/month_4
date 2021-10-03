from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MovieListSerializer, ProductsSerialzer
from main.models import Movie, Product, Category, Tag, Review

@api_view(['GET'])
def print_hello(request):
    context = {
        'text': 'hello world',
        'number': 123456,
        'boolean': False,
        'float': 14.1,
        'list': [1,2,3,4,5],
    }
    return Response(data=context, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def movies_list_view(request):
    movies = Movie.objects.all()
    data = MovieListSerializer(movies, many=True).data
    return Response(data=data)

@api_view(['GET'])
def movies_item_view(request, pk):
    try:
        movie = Movie.objects.get(id=pk)
    except Movie.DoesNotExist:
        return Response(data={'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    data = MovieListSerializer(movie).data
    return Response(data=data)

@api_view(['GET'])
def products(request):
    product = Product.objects.all()
    data = ProductsSerialzer(product, many=True).data
    return Response(data=data)

@api_view(['GET'])
def product_items(request, pk):
    try:
        product =  Product.objects.get(tags=pk)
    except Product.DoesNotExist:
        return Response(data={'message':'Could not find anything by this tag'}, status=status.HTTP_404_NOT_FOUND)
    data = ProductsSerialzer(product).data
    return Response(data=data)

