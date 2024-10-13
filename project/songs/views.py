from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Songs, UserSongsRating
from .serializers import SongsSerializer, UserSongsRatingSerializer, UserRatedSongSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.db.models import Q

class SongsPagination(PageNumberPagination):
    """Custom pagination class."""
    page_size = 10  
    page_size_query_param = 'page_size'  
    max_page_size = 100  
    
class SongsListView(generics.ListAPIView):
    """API view to retrieve a list of songs with pagination."""
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    pagination_class = SongsPagination


# TODO
# Later we can add full text search or elastic search for songs
class SongsSearchView(generics.ListAPIView):
    serializer_class = SongsSerializer
    pagination_class = SongsPagination

    def get_queryset(self):
        title = self.request.query_params.get('title', None)
        if title:
            return Songs.objects.filter(title__icontains=title) # Like "yo yo honey"
        return Songs.objects.all()  
    

class RatingView(generics.CreateAPIView):
    serializer_class = UserSongsRatingSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  

        existing_rating = UserSongsRating.objects.filter(
            user=request.user,
            song=data['song']
        ).first()

        if existing_rating:
            serializer = self.get_serializer(existing_rating, data=data, partial=True)
        else:
            serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_200_OK if existing_rating else status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRatedSongsView(generics.ListAPIView):
    serializer_class = UserRatedSongSerializer
    permission_classes = [permissions.IsAuthenticated]  
    pagination_class = SongsPagination

    def get_queryset(self):
        user = self.request.user
        print(UserSongsRating.objects.filter(user=user))
        return UserSongsRating.objects.filter(user=user)
    

class QuerySongsView(generics.ListAPIView):
    serializer_class = SongsSerializer
    pagination_class = SongsPagination

    def get_queryset(self):
        queryset = Songs.objects.all()
        filters = Q()

        query = self.request.query_params.getlist('query')
        print(query)

        for param in query:
            try:
                field, operator, value = param.split(':')
            except ValueError:
                raise ValidationError("param must be in the format 'field:operator:value'.")

            if field not in [
                'danceability', 'energy', 'loudness', 'acousticness',
                'instrumentalness', 'liveness', 'valence', 'tempo',
                'duration_ms']:
                raise ValidationError(f"Invalid field: {field}")

            if operator not in ['gt', 'lt', 'lte', 'gte']:
                raise ValidationError(f"Invalid operator {operator}")


            filters &= Q(**{f"{field}__{operator}": value})

        return queryset.filter(filters)