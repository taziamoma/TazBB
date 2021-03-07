from django.contrib import admin
from .models import Category, Forum, Thread, Post

# Register your models here.
admin.site.register(Category)
admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(Post)