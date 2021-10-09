from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MovieListSerializer, ProductsSerialzer, PrReviewsSerializer, PrTagSerializer, CreateMovieValidateSerializer
from main.models import Movie, Product, Category, Tag, Review, PrReviews, PrTag


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

@api_view(['GET', 'POST'])
def movies_list_view(request):
    if request.method == 'POST':
        serializer = CreateMovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={'message': 'error', 'errors': serializer.errors}
            )
        name = request.data.get('name', '')
        duration = request.data.get('duration', 0)
        date = request.data.get('date', '')
        age_restriction = request.data.get('age_restriction', '')
        movie = Movie.objects.create(name=name, duration=duration,
                                     date=date, age_restriction=age_restriction)
        movie.genres.set(request.data['genres'])
        movie.save()
        return Response(data={'message': 'you created movie!',
                              'movie': MovieListSerializer(movie).data})
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

@api_view(['GET'])
def product_reviews(request):
    review = PrReviews.objects.all()
    data = PrReviewsSerializer(review, many=True).data
    return Response(data=data)


@api_view(['GET'])
def product_tags(request):
    tag = PrTag.objects.all()
    data = PrTagSerializer(tag, many=True).data
    return Response(data=data)

@api_view(['GET', 'PUT', 'DELETE'])
def product_id_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'message': 'There are no such products'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        product.delete()
        return Response(data={'message': 'Product has been removed successfully'})
    elif request.method == 'PUT':
        product.name = request.data.get('name')
        product.description = request.data.get('description')
        product.category = request.data.get('category')
        product.tags.set(request.data['tags'])
        product.price = request.data.get('price')
        product.save()
        return Response(data={'message': 'Product has been saved successfully',
                              'product': ProductsSerialzer(product).data})

    data = ProductsSerialzer(product, many=False).data
    return Response(data=data)



