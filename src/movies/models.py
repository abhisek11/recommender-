from django.db import models

# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_lenth=120, unique=True)
    overview = models.TextField()
    release_date = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
