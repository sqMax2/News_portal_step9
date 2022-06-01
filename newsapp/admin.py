from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

from .models import Author, Category, Post, Comment, CategorySubscribers


class CategoryInline(admin.StackedInline):
    model = Category.subscribers.through
    # filter_horizontal = ('categories',)
    extra = 1


class CategoryAdmin(ModelAdmin):
    list_display = ('name', )
    inlines = [CategoryInline]


admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post)
admin.site.register(Comment)

