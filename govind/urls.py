"""
URL configuration for govind project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# ---------------------------------------------------------------------------
# Lightweight health-check endpoint for uptime monitoring (e.g. UptimeRobot).
# Returns HTTP 200 "OK" instantly — no DB, no auth, no templates.
# ---------------------------------------------------------------------------
@csrf_exempt
def health_check(request):
    return HttpResponse("OK", content_type="text/plain", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health-check'),  # uptime monitoring
    path('', include('school.urls')),
    path('manager/', include('Appadmin.urls')),
]

# Serve static files (always — WhiteNoise handles production)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files locally ONLY during development.
# In production, Cloudinary delivers media files directly via CDN.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)