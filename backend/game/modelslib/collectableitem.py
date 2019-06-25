from django.db import models

# Create your models here.

class CollectableItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    class_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title
