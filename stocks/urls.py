from django.urls import path
from .views import (
    DisinfectantProductionView,
    MaterialView,
    DisinfectantListCreateView,
    DisinfectantRecipeListCreateView,
    DisinfectantRecipeUpdateView,
    DisinfectantRecipeDeleteView,
)



from rest_framework.routers import DefaultRouter
from .api_views import MaterialViewSet, DisinfectantViewSet 
from django.urls import path, include

router = DefaultRouter()
router.register(r'materials', MaterialViewSet)
router.register(r'disinfectants', DisinfectantViewSet)



urlpatterns = [
    path('api/', include(router.urls)),
    path('api/produce/', DisinfectantProductionView.as_view(), name='produce_disinfectant'),  # ✅ DÜZENLENDİ
    path('api/recipes/', DisinfectantRecipeListCreateView.as_view(), name='recipe_list_create'),
    path('api/materials/', MaterialView.as_view(), name='material_create_or_update'),
    path('api/recipes/<int:pk>/update/', DisinfectantRecipeUpdateView.as_view(), name='recipe_update'),
    path('api/recipes/<int:pk>/delete/', DisinfectantRecipeDeleteView.as_view(), name='recipe_delete'),
]