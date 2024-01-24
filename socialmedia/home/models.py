from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="posts")
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=50)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated", "-date_posted")

    def __str__(self) -> str:
        return f"{self.title} - {self.user}"
    
    def get_absolute_url(self):
        return reverse("home:post_detail", args=(self.id, self.slug))