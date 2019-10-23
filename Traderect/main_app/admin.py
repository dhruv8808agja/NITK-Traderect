from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Need)
admin.site.register(Photos)
admin.site.register(Products)
admin.site.register(Renttransaction)
admin.site.register(Rentad)
admin.site.register(Sellad)
admin.site.register(Users)
admin.site.register(Wishes)
