# Django core imports
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# Local app imports

from accounts import views as user_views
from .views import (
    profile_create,
    ProfileListView,
    ProfileUpdateView,
    CustomerListView,
    CustomerCreateView,
    CustomerUpdateAPIView,
    CustomerDeleteAPIView,
    ProfileUpdateView,
    get_customers,
    ProfileDeleteAPIView,
    vendor_list,
    vendor_create,
    vendor_delete,
    vendor_update,
    dashboard,
    current_user
)
from rest_framework.urlpatterns import format_suffix_patterns

# en başta tanımlanan URL'ler
urlpatterns = [
    # User authentication URLs
    path('register/', user_views.register, name='user-register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'), name='user-login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', user_views.Profile, name='user-profile'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='accounts/logout.html'), name='user-logout'),
    path('api/user/', current_user, name='current-user'),

    # Profile URLs
    path('profiles/', ProfileListView.as_view(), name='profile_list'),
    path('new-profile/', user_views.profile_create, name='profile_create'),
    path('profile/<int:pk>/update/',  ProfileUpdateView.as_view(),
         name='profile-update'),
    path('profiles/<int:pk>/delete/', ProfileDeleteAPIView.as_view(), name='api-profile-delete'),

    # Customer URLs
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', user_views.CustomerCreateView,
         name='customer_create'),
    path('customers/<int:pk>/update/', CustomerUpdateAPIView.as_view(), name='customer-update'),
    path('customers/<int:pk>/delete/', CustomerDeleteAPIView.as_view(), name='customer-delete'),
    path('get_customers/', get_customers, name='get_customers'),

    path('vendors/', views.vendor_list, name='vendor-list'),
    path('vendors/new/', views.vendor_create, name='vendor-create'),
    path('vendors/<int:pk>/update/', views.vendor_update, name='vendor-update'),
    path('vendors/<int:pk>/delete/', views.vendor_delete, name='vendor-delete'),
]

from rest_framework.routers import DefaultRouter
from .api_views import CustomerViewSet, VendorViewSet, ProfileViewSet  
from django.urls import path, include
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'vendors', VendorViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns += [
    path('api/', include(router.urls)),
]
