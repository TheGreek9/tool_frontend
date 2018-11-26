from django import forms


class CaseForm(forms.Form):
    caseclient = forms.Select()
    casename = forms.Select()
    firm_file_number = forms.Select()
    court_case_number = forms.Select()
    doi = forms.Select()
    criticalnote = forms.Select()
