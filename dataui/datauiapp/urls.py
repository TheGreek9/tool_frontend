from django.urls import path

from .views import IndexView, DetailsView
from . import views


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('details/<slug:file_name>/', DetailsView.as_view(), name='details')
]