from django.contrib import admin
from .models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "date_posted", "updated")
    search_fields = ("title", "content", "user")
    list_filter = ("updated", "date_posted")
    prepopulated_fields = {"slug":("content",)}
    raw_id_fields = ("user",)

# admin.site.register(Post)