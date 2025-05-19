from rest_framework import viewsets
from .models import Category, Item, Delivery
from .serializers import CategorySerializer, ItemSerializer, DeliverySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API view for viewing and editing categories.
    """
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'])
    def get_categories(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ItemViewSet(viewsets.ModelViewSet):
    """
    API view for viewing and editing items.
    """
    permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=False, methods=['get'])
    def search_items(self, request):
        name = request.query_params.get('name', None)
        category_id = request.query_params.get('category', None)
        
        items = Item.objects.all()
        
        if name:
            items = items.filter(name__icontains=name)
        if category_id:
            items = items.filter(category_id=category_id)

        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class DeliveryViewSet(viewsets.ModelViewSet):
    """
    API view for viewing and editing deliveries.
    """
    permission_classes = [IsAuthenticated]
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    @action(detail=True, methods=['get'])
    def mark_as_delivered(self, request, pk=None):
        """
        Mark a delivery as delivered.
        """
        delivery = self.get_object()
        delivery.is_delivered = True
        delivery.save()
        return Response({'status': 'Delivery marked as delivered'})
