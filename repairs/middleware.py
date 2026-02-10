"""Middleware - login va ustaxona tekshiruvi"""
from django.shortcuts import redirect


class ShopMiddleware:
    """Har bir so'rovda request.shop ni o'rnatadi. Login talab qiladi."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        if request.path in ('/', '/register/', '/logout/'):
            return self.get_response(request)

        if not request.user.is_authenticated:
            from urllib.parse import quote
            return redirect('/?next=' + quote(request.path))

        if hasattr(request.user, 'shop_profile'):
            request.shop = request.user.shop_profile.shop
        else:
            return redirect('/register/?msg=profil')

        return self.get_response(request)
