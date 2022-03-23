from django.db import models

# Create your models here.
class FileUpload(models.Model):
    fileurl=models.TextField(default=None)
