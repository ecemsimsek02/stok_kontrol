from django.urls import path
from .views import BillListCreateView, BillRetrieveUpdateDestroyView

urlpatterns = [
    path('bills-list/', BillListCreateView.as_view(), name='bill_list'),
    path('bills-detail/<int:pk>/', BillRetrieveUpdateDestroyView.as_view(), name='bill-detail'),
]


from rest_framework.routers import DefaultRouter
from .api_views import BillViewSet 
from django.urls import path, include

router = DefaultRouter()
router.register(r'bills', BillViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]