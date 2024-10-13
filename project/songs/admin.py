from django.contrib import admin
from .models import Songs, UserSongsRating

@admin.register(Songs)
class SongAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'title', 
        'danceability', 
        'energy', 
        'key', 
        'loudness', 
        'mode', 
        'acousticness', 
        'instrumentalness', 
        'liveness', 
        'valence', 
        'tempo', 
        'duration_ms', 
        'time_signature', 
        'num_bars', 
        'num_sections', 
        'num_segments', 
        'classification',
    )
    search_fields = ('title',)
    list_filter = ('key', 'mode')
    ordering = ('title',)


class UserSongsRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'rating')  
    list_filter = ('rating', 'user', 'song')  
    search_fields = ('user__username', 'song__title')  
    ordering = ('-rating',)  


admin.site.register(UserSongsRating, UserSongsRatingAdmin)