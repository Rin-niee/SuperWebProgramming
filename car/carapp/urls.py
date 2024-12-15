from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "index"), #главная
    path('auto/', views.auto, name = "auto"), #страница авто
    path('catalog/<str:country>/', views.catalog, name = "catalog"), #каталог
    path('promotion/', views.promotion, name = "promotion"), #акции
    path('contacts/', views.contacts, name = "contacts"), #контакты
    path('workconditions/', views.workconditions, name = "workconditions"), #условия работы

]