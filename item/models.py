from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title
