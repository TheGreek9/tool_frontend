from django.urls import path

from .views import FileView, DetailsView, NextFileView, IndexView
from . import views


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('cases/', FileView.as_view(), name='cases'),
    path('contacts/', NextFileView.as_view(), name='contacts'),
    path('details/<slug:file_name>/', DetailsView.as_view(), name='details')
]