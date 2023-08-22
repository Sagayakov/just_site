from django.contrib import admin
from .models import RealEstateModel


@admin.register(RealEstateModel)
class RealEstateAdmin(admin.ModelAdmin):
    pass
