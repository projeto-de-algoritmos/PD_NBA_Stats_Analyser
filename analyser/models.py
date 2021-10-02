from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=50)
    team_id = models.PositiveIntegerField()
    abbreviation = models.CharField(max_length=3)
