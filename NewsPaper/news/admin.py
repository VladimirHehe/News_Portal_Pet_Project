from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class PostAdmin(admin.ModelAdmin):
    search_fields = ['text']


class CategoryAdmin(TranslationAdmin):
    model = Category
    fields = ('title',)


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Subscription)
