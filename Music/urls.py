from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from Music.views import home_base,login_redirect

urlpatterns = [
    path('', home_base, name="home_base"),
    path('admin/', admin.site.urls),
    path('ngoma/', include('ngoma.urls')),
    path('accounts/profile/',login_redirect)
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
