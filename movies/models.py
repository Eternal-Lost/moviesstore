from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
    
class Petition(models.Model):
    title = models.CharField(max_length=255)
    created_by_user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    votes = models.ManyToManyField(User, related_name = 'petition_votes', blank = True)

    def vote_count(self):
        return self.votes.count()
    
    vote_count = property(vote_count)

    def user_voted(self, user):
        return self.votes.filter(id = user.id).exists()
    
    def __str__(self):
        return f"Petition {self.id} - {self.title}"