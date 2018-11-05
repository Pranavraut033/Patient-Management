from django import forms
from .models import *
# from django.contrib.admin.widgets import AdminDateWidget, ForeignKeyRawIdWidget
# from django.core.exceptions import ObjectDoesNotExist
# from django.db.models.fields.reverse_related import ManyToOneRel
# from django.db.models.fields.related import OneToOneField
# from django.db.models.fields import AutoField
# import clinic.utils.validators as v
# import clinic.utils.constants as consts


class LoginForm(forms.Form):
    username = forms.CharField(validators=[v.validate_username_login])
    password = forms.CharField(validators=[v.validate_password])

# def getValue(self, field):
#     return self[field].value()
#
# exceptions = [ManyToOneRel, AutoField, OneToOneField]
#
# def save_object(self, object_class, to_commit, *exclude, **extra):
#     fields = object_class._meta.get_fields()
#     attrs = [x.attname for x in fields if (type(x) not in exceptions and x.attname not in exclude)]
#     values = {x : getValue(self, x) for x in attrs}
#     values = {**values, **extra}
#     obj = object_class(**values)
#     if to_commit: obj.save()
#     return obj;
# class AddressForm(forms.Form):
#
#     class Meta:
#         model = Address
#         exclude = ['id']
# class GenericForm(forms.ModelForm):
#     # TODO: fix profile field not saving
#
#     class Meta:
#         model = Person
#         exclude = ['reg_time', 'id']
# class DoctorForm(LoginForm, GenericForm):
#     username = forms.CharField(validators=[v.validate_username_create])
#     confirm_pass = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
#
#     speciality  = forms.ChoiceField(choices=consts.specialties, initial='gp')
#     qual = forms.CharField(label="Qualification", max_length=20, required=False)
#     bio = forms.CharField(label='Biography', required=False)
#
#     def __str__(self):
#         return getValue(self, "username")
#
#     def save(self, commit=True):
#         if not self.is_valid():
#             raise Exception("The form has invalid fields" + str(self.errors))
#
#         if not getValue(self, 'password') == getValue(self, 'confirm_pass'):
#             ex = Exception('Passwords doesn\'t match!')
#             ex.data = {'confirm_pass' : 'Passwords doesn\'t match!'}
#             raise ex
#
#         return save_object(self, Doctor, commit, 'reg_time', 'id')
# class PatientForm(GenericForm, forms.ModelForm):
#     class Meta:
#         model = Patient
#         exclude = ['reg_time', 'id', 'registered_by_id', 'registered_by']
#
#     def save(self, doctor, commit=True):
#         return save_object(self, Patient, commit, *self.Meta.exclude, registered_by=doctor)
#
#     def __str__(self):
#         return getValue(self, "first_name") + getValue(self, "last_name")
# class CaseForm(forms.ModelForm):
#
#     class Meta:
#         model = Patient
#         exclude = []
#
#     def __str__(self):
#         return 'Case'
#
# class ApptForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         exclude = []
#
#     def __str__(self):
#         return 'Appointment'
