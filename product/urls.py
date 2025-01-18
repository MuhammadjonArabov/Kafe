from django.urls import path
from .views import order_view

app_name='product'
urlpatterns = [
    path('signup', order_view, name='signup'),
]