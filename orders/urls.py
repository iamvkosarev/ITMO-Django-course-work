from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.list, name='list_of_orders'),
    url(r'^add$', views.add, name='add_order'),
    path('<int:id>/', views.dynamic_lookup_view, name='order'),
]
