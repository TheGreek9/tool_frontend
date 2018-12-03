from django import forms

from .models import CaseModel, ClientModel

case_model_fields = [a.name for a in CaseModel._meta.get_fields()]
client_model_fields = [a.name for a in ClientModel._meta.get_fields()]


class CaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices') if kwargs.get('choices') else None
        super(CaseForm, self).__init__(*args, **kwargs)
        if choices:
            for field in case_model_fields:
                self.fields[field] = forms.ChoiceField(choices=choices)

class ClientForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for field in client_model_fields:
            self.fields[field] = forms.ChoiceField(choices=choices)