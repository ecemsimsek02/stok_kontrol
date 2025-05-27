from rest_framework import status, views
from rest_framework.response import Response
from .models import Disinfectant, DisinfectantRecipe
from .serializers import DisinfectantProductionSerializer
from rest_framework import generics
from .models import Material, Disinfectant, DisinfectantRecipe
from .serializers import MaterialSerializer, DisinfectantSerializer, DisinfectantRecipeSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.db.models import F
class DisinfectantProductionView(views.APIView):
    """View for producing disinfectants and updating the stock."""
    
    def post(self, request, *args, **kwargs):
        serializer = DisinfectantProductionSerializer(data=request.data)
        if serializer.is_valid():
            disinfectant_id = serializer.validated_data['disinfectant_id']
            quantity_to_produce = serializer.validated_data['quantity_to_produce']

            disinfectant = Disinfectant.objects.get(id=disinfectant_id)
            recipes = DisinfectantRecipe.objects.filter(disinfectant=disinfectant)

            for recipe in recipes:
                material_needed = recipe.quantity * quantity_to_produce
                material = recipe.material

                if material.quantity_in_stock < material_needed:
                    return Response(
                        {"error": f"Yetersiz stok: {material.name} (Gerekli: {material_needed}, Mevcut: {material.quantity_in_stock})"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Malzeme stoklarını düşür
            for recipe in recipes:
                recipe.material.quantity_in_stock -= recipe.quantity * quantity_to_produce
                recipe.material.save()

            # Dezenfektan stok artır
            disinfectant.update_stock(quantity_to_produce)

            return Response({"message": "Dezenfektan üretildi, stoklar güncellendi."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DisinfectantListCreateView(generics.ListCreateAPIView):
    queryset = Disinfectant.objects.all()
    serializer_class = DisinfectantSerializer

class DisinfectantRecipeListCreateView(generics.ListCreateAPIView):
    queryset = DisinfectantRecipe.objects.all()
    serializer_class = DisinfectantRecipeSerializer

class DisinfectantRecipeUpdateView(generics.UpdateAPIView):
    queryset = DisinfectantRecipe.objects.all()
    serializer_class = DisinfectantRecipeSerializer

class DisinfectantRecipeDeleteView(generics.DestroyAPIView):
    queryset = DisinfectantRecipe.objects.all()
    serializer_class = DisinfectantRecipeSerializer

class MaterialView(APIView):
    def post(self, request):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            # Get or create the material
            name = serializer.validated_data['name']
            quantity = serializer.validated_data['quantity_in_stock']
            unit = serializer.validated_data['unit']
            
            material = Material.create_or_update_material(name, quantity, unit)
            
            return Response({'message': f'Material {material.name} updated successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockAlertView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        material_alerts = Material.objects.filter(quantity_in_stock__lt=F('min_stock_level'))
        disinfectant_alerts = Disinfectant.objects.filter(quantity_in_stock__lt=F('min_stock_level'))

        alerts = []

        for m in material_alerts:
            alerts.append(f"Malzeme '{m.name}' minimum stok seviyesinin altında.")

        for d in disinfectant_alerts:
            alerts.append(f"Dezenfektan '{d.name}' minimum stok seviyesinin altında.")

        return Response({"alerts": alerts})