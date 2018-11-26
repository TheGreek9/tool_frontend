import csv
import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from collections import namedtuple
from django.urls import reverse
from django.views import View

from .models import ClientModel, CaseModel

super_long_dicts = {}


class IndexView(View):
    def get(self, request):
        return render(request, 'datauiapp/index.html')

    def post(self, request):
        if not any(super_long_dicts):
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse("Bewbs")


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
    CSVRow = None
    model_fields = None
    next_uri = None

    def get(self, request, *args, **kwargs):
        self.file_path = get_file_path(kwargs)
        self.CSVRow = get_csv_tuples(self.file_path)
        context = {
            'csv_col_list': self.CSVRow._fields,
            'model_fields': self.model_fields,
            'file_name': kwargs.get('file_name'),
            'next_uri': self.next_uri
        }
        return render(request, 'datauiapp/csv_table_2.html', context)

    def post(self, request, *args, **kwargs):
        giant_dict = {}
        for field in self.model_fields:
            if request.POST[field]:
                giant_dict.update({field: request.POST[field]})

        self.attach_dicts(super_long_dicts, giant_dict)

        return HttpResponseRedirect(reverse('index'))

    def attach_dicts(self, major_dict, tiny_dict):
        pass


class CasesDetailView(ColumnDetailsView):
    model_fields = [a.name for a in CaseModel._meta.get_fields()]
    next_uri = 'case_details'

    def attach_dicts(self, major_dict, tiny_dict):
        major_dict.update({'case_file_path': self.file_path,
                           'case_dict': tiny_dict})


class ClientsDetailView(ColumnDetailsView):
    model_fields = [a.name for a in ClientModel._meta.get_fields()]
    next_uri = 'client_details'

    def attach_dicts(self, major_dict, tiny_dict):
        major_dict.update({'client_file_path': self.file_path,
                           'client_dict': tiny_dict})


def get_file_path(kwargs_dict):
    return os.path.join('/Users/Spyro/Developer/graphql_ui',
                        '{}.csv'.format(kwargs_dict.get('file_name')))


def get_csv_tuples(file_path):
    header_cols = [a for a in csv.reader(open(file_path, "r"))][0]
    return namedtuple('CSVRow', header_cols)


def get_csv_rows(file_path):
    CSVRow = get_csv_tuples(file_path)
    return [CSVRow._make(a) for a in csv.reader(open(file_path, "r"))][1:]


def attach_client_info(client_id, client_mapping, client_file_path):
    csv_rows = get_csv_rows(client_file_path)
    for row in csv_rows:
        pass
    return dict()
