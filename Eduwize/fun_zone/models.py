from django.db import models

class Hackathon(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    prize = models.CharField(max_length=100)

    def __str__(self):
        return self.title