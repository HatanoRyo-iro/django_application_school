from django.contrib import admin

from .models import Post, Group, Friend, Good

# Register your models here.

admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Friend)
admin.site.register(Good)