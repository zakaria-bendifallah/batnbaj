from django.contrib import admin
from .models import Category, Story, Character, Response
# Register your models here.

admin.site.register(Category)
admin.site.register(Story)
admin.site.register(Character)
admin.site.register(Response)
