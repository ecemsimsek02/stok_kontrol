from rest_framework import viewsets
from .models import Material, Disinfectant
from .serializers import MaterialSerializer, DisinfectantSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class DisinfectantViewSet(viewsets.ModelViewSet):
    queryset = Disinfectant.objects.all()
    serializer_class = DisinfectantSerializer
