from django.contrib import admin
from dgunotice.models import Category, User, Keyword, Notice

# Register your models here.
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Keyword)
admin.site.register(Notice)