from django.contrib import admin
from . import models


class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'views', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'views', 'likes']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(models.Page, PageAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.UserProfile)