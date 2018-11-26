from django.urls import path

from .views import FileView, ColumnDetailsView, ContactsFileView, IndexView, \
    CasesFileView, CasesDetailView, ClientsDetailView
from . import views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('cases/', CasesFileView.as_view(), name='cases'),
    path('contacts/', ContactsFileView.as_view(), name='contacts'),
    path('casedetails/<slug:file_name>/', CasesDetailView.as_view(),
         name='case_details'),
    path('clientdetails/<slug:file_name>/', ClientsDetailView.as_view(),
         name='client_details'),
]
