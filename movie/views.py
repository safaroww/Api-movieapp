from django.shortcuts import get_object_or_404
from .models import Studio, Genre, Movie
from rest_framework.response import Response
from rest_framework import status, generics, parsers, permissions, pagination, filters
from rest_framework.decorators import api_view, parser_classes
from .serializers import StudioSerializer, GenreSerializer, MovieSerializer
from user.permissions import IsAdminOrReadOnly
from .permissions import DirectorPermission
from .paginations import GenrePagination, GenreCursorPagination
from user.throttlings import User10ForMinute, Anon5ForMinute
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MovieFilter

# Create your views here.


# @api_view(['GET', 'POST'])
# def studio_list(request):
#     if request.method == 'GET':
#         studios = Studio.objects.all()
#         serializer = StudioSerializer(instance=studios, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = StudioSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        



# @api_view(['GET', 'PUT', 'DELETE'])
# def studio_detail(request, pk):
#     studio = get_object_or_404(Studio, pk=pk)
#     if request.method == 'GET':
#         serializer = StudioSerializer(instance=studio)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = StudioSerializer(instance=studio, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#     elif request.method == 'DELETE':
#         studio.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




class StudioListAV(generics.ListCreateAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    permission_classes = [IsAdminOrReadOnly]


class StudioDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    permission_classes = [DirectorPermission]



class GenreListAV(generics.ListCreateAPIView):
    def get_queryset(self): 
        # self.request
        # self.kwargs
        # self.query_params
        return Genre.objects.all()
    def get_serializer_class(self):
        return GenreSerializer
    pagination_class = GenrePagination
    # pagination_class = pagination.LimitOffsetPagination
    # pagination_class = GenreCursorPagination
    throttle_classes = [User10ForMinute, Anon5ForMinute]


class GenreDetailAV(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Genre.objects.all()
    def get_serializer_class(self):
        return GenreSerializer
    



class MovieListAV(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # filterset_fields = ['director', 'genres']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'
    search_fields = ['title', 'director__user__username', 'description', 'director__studio__title']
    filterset_class = MovieFilter

class MovieDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer



class MovieFormUpdateAV(generics.UpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]