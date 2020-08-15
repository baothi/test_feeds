from django.urls import path, include
from . import views

urlpatterns= [
    path('', views.index, name='index'),
    path('update_product/<pk>', views.UpdateProduct, name='update-product'),
    path('delete_product/<pk>', views.DeleteProduct, name='delete-product'),
]