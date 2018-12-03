import csv
import json
import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from collections import namedtuple
from django.urls import reverse
from django.views import View

from .forms import CaseForm, ClientForm
from .helpers import get_csv_rows, \
    attach_client_info, get_file_path, get_csv_tuples
from .models import ClientModel, CaseModel

super_long_dicts = {}


class IndexView(View):
    def get(self, request):
        return render(request, 'datauiapp/index.html')

    def post(self, request):
        if not any(super_long_dicts):
            return HttpResponseRedirect(reverse('index'))
        else:
            case_dict = super_long_dicts.get('case_dict')
            client_dict = super_long_dicts.get('client_dict')

            new_dict = {}
            for key, val in case_dict.items():
                if key == 'caseclient':
                    new_dict.update({'caseclient': client_dict})
                else:
                    new_dict.update({key: val})

            response = HttpResponse(json.dumps(new_dict))
            response['Content-Type'] = 'application/json'
            response['Content-Length'] = len(str(new_dict))
            response['Content-Disposition'] = 'attachment; ' \
                                              'filename=json_test.json'

            return response

class FileView(View):
    next_uri = None
    reverse_uri = None
    model_name = None

    def get(self, request):
        content = dict(next_uri=self.next_uri,
                       model_name=self.model_name)
        return render(request, 'datauiapp/cases.html', content)

    def post(self, request):
        file_name = request.POST['csv_file'].split('.csv')[0]
        related_file = request.POST['related_file'].split('.csv')[0] if \
            request.POST['related_file'] else 'None'
        next_kwargs = dict(file_name=file_name, related_file=related_file)
        return HttpResponseRedirect(reverse(self.reverse_uri,
                                            kwargs=next_kwargs))


class CasesFileView(FileView):
    next_uri = 'cases'
    reverse_uri = 'case_details'
    model_name = 'Case'


class ContactsFileView(FileView):
    next_uri = 'contacts'
    reverse_uri = 'client_details'
    model_name = 'Client'


class ColumnDetailsView(View):
    file_path = None
    header_cols = None
    CSVRow = None
    model_fields = None
    next_uri = None
    related_file = None

    def get(self, request, *args, **kwargs):
        self.file_path = get_file_path(kwargs)
        self.CSVRow = get_csv_tuples(self.file_path)._fields
        choices = tuple(enumerate(self.CSVRow, start=1))
        case_form = CaseForm(**dict(choices=choices))
        # case_form = CaseForm()
        # client_form = ClientForm(choices=choices)
        context = {
            'csv_col_list': self.CSVRow,
            'file_name': kwargs.get('file_name'),
            'next_uri': self.next_uri,
            'related_file': kwargs.get('related_file') if kwargs.get(
                'related_file') != 'None' else None,
            'case_form': case_form,
            # 'client_form': client_form
        }
        return render(request, 'datauiapp/csv_table_2.html', context)

    def post(self, request, *args, **kwargs):
        self.file_path = get_file_path(kwargs)
        giant_dict = {}
        linking_dict = {}
        self.CSVRow = get_csv_tuples(self.file_path)._fields
        choices = tuple(enumerate(self.CSVRow, start=1))
        form = CaseForm(request.POST, **dict(choices=choices))
        if form.is_valid():
            for key, val in form.cleaned_data.items():
                giant_dict.update({key: choices[1 - int(val)][1]})

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
