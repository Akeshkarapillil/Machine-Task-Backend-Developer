from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TagModel(models.Model):
    title = models.CharField(
        verbose_name="Tag Title",
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.title

class TextModel(models.Model):
    text_snippet = models.CharField(
        verbose_name="Short Text Snippet",
        max_length=100,
    )
    tag = models.ForeignKey(
        to="TagModel",
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


