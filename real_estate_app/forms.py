# forms.py
from django import forms
from .models import UserDetails, Unit


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class TenantRegForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        exclude = ['user_id', 'created_by', 'user_type']


class PropertyForm(forms.Form):
    property_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    features = forms.CharField(max_length=100)


class UnitForm(forms.Form):
    property = forms.IntegerField()
    rent_cost = forms.CharField(max_length=100)
    unit_type = forms.CharField(max_length=100)
    tenant = forms.IntegerField()
    agreement_end_date = forms.DateField()
