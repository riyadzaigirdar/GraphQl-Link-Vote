from django.db import models
from django.conf import settings


class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.url


class Votes(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.ForeignKey('Link', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} voted on {self.link.url}"
