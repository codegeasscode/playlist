from django.db import models
from django.conf import settings 
import pandas as pd
import json

# TODO
# we can do preprocessing to separate class which can handle other sources
# e.g., field mapping, beautiful soup, dat file

# use of pandas, in later part direct df can be passed for the same
class SongsManager(models.Manager):
    def from_json(self, json_data):
        """Store songs information from a JSON object or JSON string."""
        if isinstance(json_data, str):
            # If json_data is a string, try to parse it as JSON
            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError:
                raise Exception("Invalid JSON data")

        # Load data into a DataFrame
        df = pd.DataFrame(json_data)
        self.save_dataframe(df)

    def from_json_file(self, file_path):
        """Load songs data from a JSON file and store it in the database."""
        # Read the JSON file into a DataFrame
        df = pd.read_json(file_path)
        self.save_dataframe(df)

    def save_dataframe(self, df):
        """Save the DataFrame to the Songs model."""

        if df.empty:
            raise Exception("No data to save.")
        
        # Convert DataFrame rows to Song model instances
        songs = [
            Songs(
                uid=row['id'],
                title=row['title'],
                danceability=row['danceability'],
                energy=row['energy'],
                key=row['key'],
                loudness=row['loudness'],
                mode=row['mode'],
                acousticness=row['acousticness'],
                instrumentalness=row['instrumentalness'],
                liveness=row['liveness'],
                valence=row['valence'],
                tempo=row['tempo'],
                duration_ms=row['duration_ms'],
                time_signature=row['time_signature'],
                num_bars=row['num_bars'],
                num_sections=row['num_sections'],
                num_segments=row['num_segments'],
                classification=row['class'],
            )
            for _, row in df.iterrows()
        ]

        # Bulk create the songs in the database
        Songs.objects.bulk_create(songs)


class Songs(models.Model):
    uid = models.CharField(max_length=100, unique=True)  # Unique identifier for the song
    title = models.CharField(max_length=255)
    danceability = models.DecimalField(max_digits=6, decimal_places=4)  # e.g., 0.521
    energy = models.DecimalField(max_digits=8, decimal_places=6)  # e.g., 0.673
    key = models.IntegerField()  # e.g., 8
    loudness = models.DecimalField(max_digits=8, decimal_places=6)  # e.g., -8.685
    mode = models.IntegerField()  # e.g., 1
    acousticness = models.DecimalField(max_digits=8, decimal_places=6)  # e.g., 0.00573
    instrumentalness = models.DecimalField(max_digits=10, decimal_places=8)  # e.g., 0.000000
    liveness = models.DecimalField(max_digits=8, decimal_places=6)  # e.g., 0.1200
    valence = models.DecimalField(max_digits=8, decimal_places=6)  # e.g., 0.543
    tempo = models.DecimalField(max_digits=8, decimal_places=4)  # e.g., 108.031
    duration_ms = models.IntegerField()  # e.g., 225947
    time_signature = models.IntegerField()  # e.g., 4
    num_bars = models.IntegerField()  # e.g., 100
    num_sections = models.IntegerField()  # e.g., 8
    num_segments = models.IntegerField()  # e.g., 830
    classification = models.IntegerField()  # e.g., 1

    # custom manager
    objects = SongsManager()

    class Meta:
        verbose_name = "Song"  
        verbose_name_plural = "Songs" 

    def __str__(self):
        return self.title
    

# TODO
# adding a Playlist model, to maintain separate playlist
# Use of Thorough model, makes rating based on user session, each user can maintaing their own rating
class UserSongsRating(models.Model):
    
    class Rating(models.IntegerChoices):
        ONE = 1, "Very Bad"
        TWO = 2, "Bad"
        THREE = 3, "Neutral"
        FOUR = 4, "Good"
        FIVE = 5, "Very Good"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(Songs, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=Rating.choices)

    class Meta:
        unique_together = ('user', 'song')  
    def __str__(self):
        return f"{self.user.username} rated {self.song.title} with {self.rating}"