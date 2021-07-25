from django.contrib import admin
from .models import Profile, Thread, Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(Thread)
admin.site.register(Post)