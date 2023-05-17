from django.db import models

# Create your models here.

class RequestInfo(models.Model):
    id = models.AutoField(primary_key=True)
    prompt = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    text_status = models.CharField(max_length=10, default="Pending")
    text = models.CharField(max_length=100, blank=True, null=True)
    image_status = models.CharField(max_length=10, default="Pending")
    image_uri = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
