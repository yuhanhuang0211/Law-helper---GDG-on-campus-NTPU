from django.db import models
from django.db.models import Index

class Regulation(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    keywords = models.TextField(null=True, blank=True)
    
    class Meta:
        indexes = [
            Index(fields=['category']),
            Index(fields=['is_active']),
        ]
        
    def __str__(self):
        return self.title
