# from django.shortcuts import render
# from .models import Movie
# from django.http import JsonResponse


# def movie_list(request):
#     movies = Movie.objects.all()
#     data = {'movies': list(movies.values())}
#     return JsonResponse(data)

# def movie_details(request,id):
#     movie = Movie.objects.get(id=id)
#     data = {'movie name': movie.name}
#     return JsonResponse(data)