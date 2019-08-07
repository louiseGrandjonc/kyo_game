from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name
