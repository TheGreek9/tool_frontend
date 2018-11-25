import csv
import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from collections import namedtuple
from django.urls import reverse
from django.views import View

from .models import TestModel


class IndexView(View):
    def get(self, request):
        return render(request, 'datauiapp/index.html')

    def post(self, request):
        file_name = request.POST['csv_file'].split('.csv')[0]
        return HttpResponseRedirect(reverse('details', args=(file_name,)))


class DetailsView(View):
    file_path = None
    header_cols = None
    Headers = None
    model_fields = [a.name for a in TestModel._meta.get_fields()]

    def get(self, request, *args, **kwargs):
        self.file_path = self.get_file_path(kwargs)
        self.header_cols = self.get_header_cols()
        self.Headers = namedtuple('Headers', self.header_cols)
        context = {
            'csv_col_list': self.Headers._fields,
            'model_fields': self.model_fields,
            'file_name': 'next_test',
        }
        return render(request, 'datauiapp/csv_table.html', context)

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
