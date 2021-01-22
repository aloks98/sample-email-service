from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class Email(models.Model):
    id = models.AutoField(primary_key=True)
    to = ArrayField(models.EmailField())
    cc = ArrayField(models.EmailField())
    subject = models.TextField(max_length=100)
    email_text = models.TextField()
