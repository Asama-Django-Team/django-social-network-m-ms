from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostUpdateForm


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home/home.html", {"posts": posts})
    

class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        # user = User.objects.get(pk=post)
        return render(request, "home/post_detail.html", {"post": post})
    
class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post_delete = Post.objects.get(pk=post_id)
        if post_delete.user.id == request.user.id:
            post_delete.delete()
            messages.success(request, "Your Post Deleted Successfully", extra_tags="success")
        else:
            messages.error(request, "Your Post Wasn't Deleted", extra_tags="danger")
    
        return redirect("home:home")
    

class PostUpdateView(LoginRequiredMixin, View):
    form = PostUpdateForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post_update = Post.objects.get(pk=kwargs["post_id"])
        if not request.user.id == post_update.user.id:
            messages.error(request, "You Cant Update This Post")
            return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = self.form(instance=post)
        return render(request, "home/update.html", {"form": form})
    
    def post(self, request):
        pass


