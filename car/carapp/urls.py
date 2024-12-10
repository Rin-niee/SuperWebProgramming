from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('auto/', views.auto, name = "auto"),
    path('promotion/', views.promotion, name = "promotion"),
    path('contacts/', views.contacts, name = "contacts"),
    path('workconditions/', views.workconditions, name = "workconditions"),

]
