import uuid

from django.db import models


# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=200)
    main_address = models.CharField(max_length=1000, default="")
    sub_address = models.CharField(max_length=1000, default="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        ordering = ('created',)
