from rest_framework import serializers
from .models import Songs, UserSongsRating

class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = '__all__'  

class UserSongsRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSongsRating
        fields = ['song', 'rating', 'user']  
        
    def create(self, validated_data):
        user = validated_data.pop('user')  
        return UserSongsRating.objects.create(user=user, **validated_data)
    

class UserRatedSongSerializer(serializers.ModelSerializer):
    song = serializers.StringRelatedField()  

    class Meta:
        model = UserSongsRating
        fields = ['song', 'rating']