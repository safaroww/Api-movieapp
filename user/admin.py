from django.contrib import admin
from .models import Customer, Director, Review

# Register your models here.

admin.site.register(Customer)
admin.site.register(Director)
admin.site.register(Review)
