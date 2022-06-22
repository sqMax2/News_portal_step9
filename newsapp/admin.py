from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

from .models import Author, Category, Post, Comment, CategorySubscribers


def assignSportCategory(modeladmin, request, queryset):
    for i in queryset:
        Category.objects.get(name='Sport').posts.add(i)

assignSportCategory.short_description = 'Assign Sport category'



class CategoryInline(admin.TabularInline):
    model = Category.subscribers.through  #Category.subscribers.through
    # filter_horizontal = ('subscribers',)
    extra = 0


class CategoryAdmin(ModelAdmin):
    # list_display = ['name', ]
    # filter_vertical = ['subscribers', ]
    inlines = [CategoryInline]


class PostInline(admin.TabularInline):
    model = Post.postCategory.through
    extra = 0


class PostAdmin(ModelAdmin):
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


admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
