from django.contrib import admin
from .models import Brands
from .models import Cars

# Register your models here.

admin.site.register(Brands)
admin.site.register(Cars)