from django.contrib import admin

from home.models import AllSites

from .models import Country, Category, Solution


admin.site.register(Country)
admin.site.register(Category)
admin.site.register(Solution)
admin.site.register(AllSites)