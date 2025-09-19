from django.db import models
from django.db.models.query import QuerySet
from users.models import CustomUser
# Create your models here.

class ActiveManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Game.Status.ACTIVE)

class Game(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        NOT_ACTIVE = 'NA', 'Not_active'

    title = models.CharField(max_length=50, default='волейбол игра')
    game_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.ACTIVE)
    active = ActiveManager()
    players = models.ManyToManyField(CustomUser, blank=True)
    adress = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-game_date']

    def __str__(self) -> str:
        return self.title
    

