from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
    path('staff/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
    path('api-token-auth/', obtain_auth_token), 
    path('accounts/', include('accounts.urls')),
    #path('api/accounts/', include('accounts.urls')),
    path('invoice/', include('invoice.urls')),
    path('bills/', include('bills.urls')),
    path('stocks/',include('stocks.urls')),
    path('cash/',include('cash.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


