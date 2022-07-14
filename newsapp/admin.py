from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from modeltranslation.admin import TranslationAdmin

from .models import Author, Category, Post, Comment, CategorySubscribers, PostCategory


def assignSportCategory(modeladmin, request, queryset):
    for i in queryset:
        Category.objects.get(name='Sport').posts.add(i)


assignSportCategory.short_description = 'Assign Sport category'


class CategoryInline(admin.TabularInline):
    model = CategorySubscribers  #Category.subscribers.through
    # filter_horizontal = ('subscribers',)
    extra = 0
    verbose_name = 'Subscriber'


class PostInline(admin.TabularInline):
    model = PostCategory
    extra = 0
    verbose_name = 'Category'
    verbose_name_plural = 'Categories'


class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'subscribers_count', 'post_count', ]
    # filter_vertical = ['subscribers', ]
    inlines = [CategoryInline]


class PostAdmin(TranslationAdmin):
    # list_display = ['title', ]
    inlines = [PostInline]
    # filter_horizontal = ['postCategory', ]
    # fields = ('title', 'author', 'text', 'categoryType', )
    list_display = ['id', 'title', 'dateCreation', 'author', 'author_email', 'categoryType', 'no_category',
                    'category_list', ]
    list_display_links = ['title']
    list_filter = ['categoryType', 'postCategory']
    radio_fields = {'categoryType': admin.VERTICAL}
    search_fields = ['author__authorUser__username']
    actions = [assignSportCategory]

    @admin.display(description="Author's email")
    def author_email(self, obj):
        return obj.author.authorUser.email


class AuthorAdmin(ModelAdmin):
    list_display = ['authorUser', 'email', 'id', 'ratingAuthor', ]


class CommentAdmin(ModelAdmin):
    list_display = ['__str__', 'commentUser', 'rating', 'commentPost', ]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
