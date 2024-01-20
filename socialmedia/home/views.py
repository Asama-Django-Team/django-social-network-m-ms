from django.shortcuts import render
from django.views import View
from .models import Post
from django.contrib.auth.models import User


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home/home.html", {"posts": posts})
    

class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        # user = User.objects.get(pk=post)
        return render(request, "home/post_detail.html", {"post": post})

# Create your views here.
