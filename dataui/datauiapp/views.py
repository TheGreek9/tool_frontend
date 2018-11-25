import csv
import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from collections import namedtuple

from django.urls import reverse

from .models import TestModel

headers = None
model_fields = [a.name for a in TestModel._meta.get_fields()]
Headers = None

def index(request):
    if request.method == 'GET':
        return render(request, 'datauiapp/index.html')
    elif request.method == 'POST':
        file_name = request.POST['csv_file'].split('.csv')[0]
        return HttpResponseRedirect(reverse('details', args=(file_name,)))


def details(request, file_name):
    file_path = os.path.join('/Users/Spyro/Developer/graphql_ui',
                             '{}.csv'.format(file_name))

    header_cols = [a for a in csv.reader(open(file_path, "r"))][0]
    Headers = namedtuple('Headers', header_cols)

    if request.method == "GET":
        context = {
            'csv_col_list': Headers._fields,
            'model_fields': model_fields,
            'file_name': file_name,
        }
        return render(request, 'datauiapp/csv_table.html', context)
    elif request.method == "POST":
        csv_rows = [Headers._make(a) for a in csv.reader(open(file_path,
                                                              "r"))][1:]

        test_list = []

        for row in csv_rows:
            giant_dict = {}
            for field in model_fields:
                field_attr = getattr(row, request.POST[field], '')
                if field_attr:
                    giant_dict.update({field: field_attr})

            test_list.append(giant_dict)

        return HttpResponse("{}".format(test_list))
