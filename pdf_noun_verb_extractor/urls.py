from django.contrib import admin
from django.urls import include, path

from api.views import HomeView

urlpatterns = [
    path('', HomeView.as_view()),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
