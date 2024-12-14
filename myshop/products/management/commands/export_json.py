import json
from django.core.management.base import BaseCommand
from django.core.serializers import serialize
from ...models import CarouselImage, Category, Product, Cart, CartItem, Review, Favorite

class Command(BaseCommand):
    help = 'Экспортирует все данные моделей в JSON файл'

    def handle(self, *args, **kwargs):
        carousel_images = CarouselImage.objects.all()
        categories = Category.objects.all()
        products = Product.objects.all()
        carts = Cart.objects.all()
        cart_items = CartItem.objects.all()
        reviews = Review.objects.all()
        favorites = Favorite.objects.all()
        data = {
            'carousel_images': serialize('json', carousel_images),
            'categories': serialize('json', categories),
            'products': serialize('json', products),
            'carts': serialize('json', carts),
            'cart_items': serialize('json', cart_items),
            'reviews': serialize('json', reviews),
            'favorites': serialize('json', favorites),
        }

        with open('data_export.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS('Данные успешно экспортированы в data_export.json'))
