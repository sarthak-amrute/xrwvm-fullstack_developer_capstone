from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name', 'description']


class CarModelAdmin(admin.ModelAdmin):
    list_display = ['car_make', 'name', 'car_type', 'year', 'dealer_id']
    list_filter = ['car_make', 'car_type', 'year']
    search_fields = ['name', 'car_make__name']


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
