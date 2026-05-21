from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.get_admin_urls() if hasattr(admin.site, 'get_admin_urls') else admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    
    path('', include('core.urls')),
    path('shopping/', include('shopping.urls')),
    path('catalog/', include('catalog.urls')),
    path('analytics/', include('analytics.urls')),
]