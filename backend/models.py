from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(max_length=100)
    game_type = models.CharField(max_length=30, null=True)
    finish_date = models.DateField(blank=True, null=True)
    diff_game = models.FloatField()
    quality_index = models.FloatField()
    team_count = models.IntegerField()
    forum_resonance = models.IntegerField()
    winner = models.CharField(max_length=100)
    team = models.ManyToManyField(Team)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=100)

    def __str__(self):
        return self.name



