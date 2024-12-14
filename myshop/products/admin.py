from django.contrib import admin
from .models import Product, CarouselImage, Category, Cart, CartItem, Review


class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('short_caption', 'image')
    fields = ('image', 'short_caption', 'full_description')


admin.site.register(Product)
admin.site.register(CarouselImage, CarouselImageAdmin)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Review)