from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateUpdateForm, CommentCreateForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home/home.html", {"posts": posts})
    

class PostDetailView(View):
    form = CommentCreateForm

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.post_instance = Post.objects.get(pk=kwargs["post_id"], slug=kwargs["post_slug"])
        return super().setup(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        # user = User.objects.get(pk=post)
        comments = self.post_instance.pcomment.filter(is_reply=False)
        return render(request, "home/post_detail.html", {"post": self.post_instance, "comments": comments, "form": self.form})
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, "Your Comment Submitted successfull", extra_tags="success")
            return redirect("home:post_detail", self.post_instance.id, self.post_instance.slug)

        
    
class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post_delete = get_object_or_404(Post, pk=post_id)
        if post_delete.user.id == request.user.id:
            post_delete.delete()
            messages.success(request, "Your Post Deleted Successfully", extra_tags="success")
        else:
            messages.error(request, "Your Post Wasn't Deleted", extra_tags="danger")
    
        return redirect("home:home")
    

class PostUpdateView(LoginRequiredMixin, View):
    form = PostCreateUpdateForm

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.post_instance = Post.objects.get(pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        post_update = self.post_instance
        if not request.user.id == post_update.user.id:
            messages.error(request, "You Cant Update This Post")
            return redirect("home:home")

        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form(instance=post)
        return render(request, "home/update.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["content"][:30])
            new_post.save()
            messages.success(request, "Your Post Updated")
            return redirect("home:post_detail", post.id, post.slug)

class PostCreateView(LoginRequiredMixin, View):
    form = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form
        return render(request, "home/post_create.html", {"form": form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["content"][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, "You Create a New Post", extra_tags="success")
            return redirect("home:post_detail", new_post.id, new_post.slug)     
        



