from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from .managers import CustomUserManager
from django.template.defaultfilters import slugify


class CustomUser(AbstractUser):
    # 'third_name', 'first_name', 'second_name', 'status'
    username = models.SlugField(_('Ник'), max_length=30, unique=True)
    first_name = models.CharField(_('Имя'), max_length=30, null=True)
    second_name = models.CharField(_('Фамилия'), max_length=30, null=True)
    email = models.EmailField(_('Адрес электронной почты'), unique=True)

    rating = models.IntegerField(default=0)

    photo = models.ImageField(default='default.jpg', upload_to='avatars')

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.photo.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.photo.path)

    STATUS_CHOICES = (
    ('S', 'Разработчик'),
    ('B', 'Модератор'),
    ('D', 'Обычный пользователь'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='D',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
    

class Team(models.Model):
    title = models.CharField(max_length=20, blank=False, unique=True)
    players = models.ManyToManyField(CustomUser, blank=True)
    team_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title


