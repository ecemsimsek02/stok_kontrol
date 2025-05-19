from django.contrib import admin
from .models import Material, Disinfectant, DisinfectantRecipe

class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity_in_stock', 'unit']
    search_fields = ['name']


class DisinfectantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'quantity_in_stock']
    search_fields = ['name']


class DisinfectantRecipeAdmin(admin.ModelAdmin):
    list_display = ['disinfectant', 'material', 'quantity']
    search_fields = ['disinfectant__name', 'material__name']

admin.site.register(Material, MaterialAdmin)
admin.site.register(Disinfectant, DisinfectantAdmin)
admin.site.register(DisinfectantRecipe, DisinfectantRecipeAdmin)
