from rest_framework import serializers
from .models import Disinfectant, Material, DisinfectantRecipe

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'quantity_in_stock', 'unit','min_stock_level',]


class DisinfectantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disinfectant
        fields = ['id', 'name', 'quantity_in_stock','min_stock_level',]


class DisinfectantRecipeSerializer(serializers.ModelSerializer):
    disinfectant = serializers.PrimaryKeyRelatedField(queryset=Disinfectant.objects.all())
    material = serializers.PrimaryKeyRelatedField(queryset=Material.objects.all())

    class Meta:
        model = DisinfectantRecipe
        fields = ['id', 'disinfectant', 'material', 'quantity']


class DisinfectantProductionSerializer(serializers.Serializer):
    disinfectant_id = serializers.IntegerField()
    quantity_to_produce = serializers.FloatField()

    def validate(self, data):
        """Ensure enough materials are available to produce the disinfectant."""
        disinfectant = Disinfectant.objects.get(id=data['disinfectant_id'])
        quantity_to_produce = data['quantity_to_produce']
        recipes = DisinfectantRecipe.objects.filter(disinfectant_id=data['disinfectant_id'])

        # Check if materials are sufficient for production
        for recipe in recipes:
            material_needed = recipe.quantity * quantity_to_produce
            if recipe.material.quantity_in_stock < material_needed:
                raise serializers.ValidationError(f"Not enough stock for material {recipe.material.name}.")
        
        return data
