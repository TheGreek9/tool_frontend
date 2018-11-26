import csv
import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from collections import namedtuple
from django.urls import reverse
from django.views import View

from .models import ClientModel, CaseModel


class IndexView(View):
    def get(self, request):
        return render(request, 'datauiapp/index.html')


class FileView(View):
    next_uri = None
    reverse_uri = None

    def get(self, request):
        return render(request, 'datauiapp/cases.html', {'next_uri':
                                                            self.next_uri})

    def post(self, request):
        file_name = request.POST['csv_file'].split('.csv')[0]
        return HttpResponseRedirect(reverse(self.reverse_uri,
                                            args=(file_name,)))


class CasesFileView(FileView):
    next_uri = 'cases'
    reverse_uri = 'case_details'


class ContactsFileView(FileView):
    next_uri = 'contacts'
    reverse_uri = 'client_details'


class ColumnDetailsView(View):
    file_path = None
    header_cols = None
    Headers = None
    model_fields = None
    next_uri = None

    def get(self, request, *args, **kwargs):
        self.file_path = self.get_file_path(kwargs)
        self.header_cols = self.get_header_cols()
        self.Headers = namedtuple('Headers', self.header_cols)
        context = {
            'csv_col_list': self.Headers._fields,
            'model_fields': self.model_fields,
            'file_name': kwargs.get('file_name'),
            'next_uri': self.next_uri
        }
        return render(request, 'datauiapp/csv_table_2.html', context)

    def post(self, request, *args, **kwargs):
        self.file_path = self.get_file_path(kwargs)
        self.header_cols = self.get_header_cols()
        self.Headers = namedtuple('Headers', self.header_cols)
        csv_rows = [self.Headers._make(a) for a in csv.reader(open(
            self.file_path, "r"))][1:]

        test_list = []
        for row in csv_rows:
            giant_dict = {}
            for field in self.model_fields:
                field_attr = getattr(row, request.POST[field], '')
                if field_attr:
                    giant_dict.update({field: field_attr})
            test_list.append(giant_dict)

        return HttpResponse("{}".format(test_list))

    def get_file_path(self, kwargs_dict):
        return os.path.join('/Users/Spyro/Developer/graphql_ui',
                            '{}.csv'.format(kwargs_dict.get('file_name')))

    def get_header_cols(self):
        return [a for a in csv.reader(open(self.file_path, "r"))][0]


class CasesDetailView(ColumnDetailsView):
    model_fields = [a.name for a in CaseModel._meta.get_fields()]
    next_uri = 'case_details'


class ClientsDetailView(ColumnDetailsView):
    model_fields = [a.name for a in ClientModel._meta.get_fields()]
    next_uri = 'client_details'