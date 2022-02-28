from django.db import models
from django.contrib.auth.models import User

class Collections(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")
    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('name', 'user',)

class Movie(models.Model):
    display_title=models.CharField(max_length=255)
    url = models.URLField()
    img_src = models.URLField()
    folders = models.ManyToManyField(Collections,through='Bookmark', blank=True)
    def __str__(self):
        return self.display_title
    
    def check_bookmarked_by(self, user):
        mov = Movie.objects.filter(folders__user=user)
        if mov.exists():
            return True
        return False


class Bookmark(models.Model):
    folder = models.ForeignKey(Collections, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='bookmarks')
    date_added = models.DateTimeField(auto_now_add=True)