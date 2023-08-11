from django.contrib import admin
from .models import Product,Category,Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name'
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
        list_display = [
            'id',
            'name'
        ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'display_tags', 'price', 'created_at', 'description')

    def display_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'tags'

