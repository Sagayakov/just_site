from django.contrib import admin
from .models import (
    LocationModel,
    MarkTransportModel,
    ModelTransportModel,
    RealEstateModel,
    EventPosterModel,
    ThemeEventModel,
    VarietyVisaModel,
    ValidityVisaModel,
    NameServiceModel,
    NameCurrencyModel,
    VisaModel,
    TransportModel,
    WorkModel,
    ServicesModel,
    BuySellModel,
    FoodModel,
    TaxiModel,
    TripModel,
    CurrencyModel
)


@admin.register(LocationModel)
class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('location',)}



@admin.register(MarkTransportModel)
class MarkTransportAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('mark_tr',)}


@admin.register(ModelTransportModel)
class ModelTransportAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('model_tr',)}


@admin.register(ThemeEventModel)
class ThemeEventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('theme',)}


@admin.register(VarietyVisaModel)
class VarietyVisaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('variety',)}


@admin.register(ValidityVisaModel)
class ValidityVisaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('validity',)}


@admin.register(NameServiceModel)
class NameServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('kind',)}


@admin.register(NameCurrencyModel)
class NameCurrencyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('currency',)}


@admin.register(CurrencyModel)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(RealEstateModel)
class RealEstateAdmin(admin.ModelAdmin):
    pass


@admin.register(VisaModel)
class VisaAdmin(admin.ModelAdmin):
    pass


@admin.register(TransportModel)
class TransportAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkModel)
class WorkAdmin(admin.ModelAdmin):
    pass


@admin.register(ServicesModel)
class ServicesAdmin(admin.ModelAdmin):
    pass


@admin.register(BuySellModel)
class BuySellAdmin(admin.ModelAdmin):
    pass


@admin.register(FoodModel)
class FoodAdmin(admin.ModelAdmin):
    pass


@admin.register(TaxiModel)
class TaxiAdmin(admin.ModelAdmin):
    pass


@admin.register(TripModel)
class TripAdmin(admin.ModelAdmin):
    pass


@admin.register(EventPosterModel)
class EventPosterAdmin(admin.ModelAdmin):
    pass
