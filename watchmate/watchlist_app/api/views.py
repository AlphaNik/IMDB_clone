from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from watchlist_app.api.pagination import (ShowCPagination, ShowLOPagination,
                                          ShowPNPagination)
from watchlist_app.api.permissons import (IsAdminOrReadOnly,
                                          ReviewUserOrReadOnly)
from watchlist_app.api.serializers import (ReviewSerializer,
                                           StreamPlatformSerializer,
                                           WatchListSerializer)
from watchlist_app.api.throttling import WatchlistThrottle
from watchlist_app.models import Review, StreamPlatform, WatchList

# class WatchListAV(APIView):
#     def get(self,request):
#         movies = WatchList.objects.all()
#         serializer = WatchListSerializer(movies,many=True,context={'request': request})
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


# class WatchListDetailAV(APIView):
#     def get(self,request,id):
#         try:
#             movie = WatchList.objects.get(id=id)
#         except WatchList.DoesNotExist:
#             return Response({'Error':f'Movie with id {id} not found'},status=status.HTTP_404_NOT_FOUND)
#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data)
    

#     def put(self,request,id):
#         movie = WatchList.objects.get(id=id)
#         serializer = WatchListSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self,request,id):
#         movie = WatchList.objects.get(id=id)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    



# class StreamPlatformAV(APIView):
#     def get(self,request):
#         platforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platforms,many=True,context={'request': request})
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


# class StreamPlatformDetailAV(APIView):
#     def get(self,request,id):
#         try:
#             movie = StreamPlatform.objects.get(id=id)
#         except StreamPlatform.DoesNotExist:
#             return Response({'Error':f'Streaming Platform with id {id} not found'},status=status.HTTP_404_NOT_FOUND)
#         serializer = StreamPlatformSerializer(movie,context={'request': request})
#         return Response(serializer.data)
    

#     def put(self,request,id):
#         movie = StreamPlatform.objects.get(id=id)
#         serializer = StreamPlatformSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self,request,id):
#         movie = StreamPlatform.objects.get(id=id)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    


# class StreamPlatformVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)


#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         stream_platform = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(stream_platform)
#         return Response(serializer.data)
    

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     def destroy(self, request, pk=None):
#         stream_platform = StreamPlatform.objects.get(id=pk)
#         stream_platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     # def update(self, request, pk=None):
#     #     pass

#     # def partial_update(self, request, pk=None):
#     #     pass

#     @action(detail=False, methods=['get'])
#     def count(self, request):
#         count = StreamPlatform.objects.all().count()
#         return Response(count)
    
#     #we need to override each and every method explicitly
#     #but i modelviewset all are taken cared of
    

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    

   
        
class ReviewListAV(ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
    
        movie = WatchList.objects.filter(pk=pk).first()
        if not movie:
            raise NotFound(f"Show with id {pk} not found.")
        
        return Review.objects.filter(watchlist = pk)
         

class ReviewCreateAV(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')

        movie_queryset = WatchList.objects.filter(pk=pk)
        if not movie_queryset.exists():
            raise NotFound(f"Show with id {pk} does not exist.")
        movie = movie_queryset.first()

        user = self.request.user
        #check if current user has given a review already or not
        review_queryset = Review.objects.filter(watchlist=movie,review_user=user)
        if review_queryset.exists():
            raise ValidationError("You already have reviewed this show")
        
        if movie.number_of_ratings == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating+ serializer.validated_data['rating'])/2
        
        movie.number_of_ratings += 1
        movie.save()
        serializer.save(watchlist=movie,review_user = user)


class ReviewDetailAV(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly|IsAdminOrReadOnly]


class AllReviewAV(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class UserReviewAV(ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user = self.request.user
        print(f'user is {user}')
        return Review.objects.filter(review_user = user.id)
        

class AllWatchListAV(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [WatchlistThrottle,AnonRateThrottle]

    def get(self,requeset):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class AllWatchListDetailAV(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self,request,id):
        try:
            movie = WatchList.objects.get(id=id)
        except WatchList.DoesNotExist:
            return Response({'Error':f'Movie with id {id} not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    

    def put(self,request,id):
        movie = WatchList.objects.get(id=id)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        movie = WatchList.objects.get(id=id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class StreamPlatformWatchListAV(ListAPIView):
    serializer_class = WatchListSerializer

    def get_queryset(self):
        print(f'inside watchlist get queryset ')
        pk = self.kwargs.get('pk')
        print(f'id of stream pk is :{pk}')
        stream_platform = StreamPlatform.objects.filter(pk=pk).first()
        if not stream_platform:
            raise NotFound(f"Stream with id {pk} not found.")
        return WatchList.objects.filter(platform = pk)
    
#============================================================================

#filtering ways

#1)filter through url and overriding get_queryset() 
class UserReviewListAV(ListAPIView):#this view's url is : 'reviews/<str:username>/
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            raise NotFound(f"User with username {username} not found.")
        return Review.objects.filter(review_user__username = username)
    


#2)filter through query params
class UserParamReviewListAV(ListAPIView):#this view's url is : 'reviews/params/
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        print(f'username is :{username}')
        if username is None:

            return Review.objects.all()
        
        user = User.objects.filter(username=username).first()
        if not user:
            raise NotFound(f"User with username {username} not found.")
        return Review.objects.filter(review_user__username = username)
    

class AllReviewListFilterAV(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','rating',]

#============================================================================
#searching on fields

class SearchShows(ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']

#ordering on fields  + pagination

class OrderingShows(ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating',]
    # pagination_class = ShowPNPagination
    # pagination_class = ShowLOPagination
    pagination_class = ShowCPagination



# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         print(f'serializer {serializer}')
#         print(f'serializer data {serializer.initial_data}')

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET', 'POST','PUT','DELETE'])
# def movie_detail(request,id):
#     #remember we are using serializers.Serialzer.
#     #we need to write logic for post (create method) for put (update method)
#     if request.method == "GET":
#         try:
#             movie = Movie.objects.get(id=id)
#         except Movie.DoesNotExist:
#             return Response({'Error': f'Movie with id {id} not Found'},status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         movie = Movie.objects.get(id=id)
#         serializer = MovieSerializer(movie,request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
        
#     elif request.method == 'DELETE':
#         movie = Movie.objects.get(id=id)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



        


