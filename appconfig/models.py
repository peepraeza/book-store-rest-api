from django.db import models


# Create your models here.
class AppConfig(models.Model):
    app_config_id = models.AutoField(primary_key=True)
    app_config_group = models.CharField(max_length=100)
    app_config_key = models.CharField(max_length=100)
    app_config_value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
