from django.contrib import admin
from .models import Category, User, Keyword, Notice, Pagetype

# Register your models here.
admin.site.register(Pagetype)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Keyword)
admin.site.register(Notice)