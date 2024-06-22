from django.urls import path

from api.views import PDFView, UploadView

urlpatterns = [
    path('test/', UploadView.as_view(), name='test'),
    path('upload/', PDFView.as_view()),
]
