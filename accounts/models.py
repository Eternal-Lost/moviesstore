from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.total_price}"
