from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget, ForeignKeyRawIdWidget
from django.core.exceptions import ObjectDoesNotExist

# todo: add styles

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class HumanForm(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    profile = forms.ImageField(required=False)
    full_name = forms.CharField(max_length=80)
    gender = forms.ChoiceField(choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ))
    phone_number = forms.IntegerField()
    dob = forms.DateField(label = "Date of Birth", widget = AdminDateWidget)
    email = forms.CharField(max_length=40, required=False)
    address = forms.CharField(max_length=200)


class DoctorForm(LoginForm, HumanForm):
    confirm_pass = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    degree = forms.CharField(max_length=80, required=False)

    def __str__(self):
        return 'Doctor'


    def save(self, commit=True):
        err_msg, d = None, None
        def getV(field):
            return self[field].value()

        try:
            Doctor.objects.get(pk=self['username'].value())
            err_msg = 'Username already exists!'
        except ObjectDoesNotExist:
            if not str(getV('username')).find(' ') == -1:
                err_msg = 'Invalid Username'
            elif not getV('password') == getV('confirm_pass'):
                err_msg = 'Passwords doesn\'t match!'
            else:
                d = Doctor(profile=getV('profile'), full_name=getV('full_name'), gender=getV('gender'), \
                        degree=getV('degree'), dob=getV('dob'), phone_number=getV('phone_number'), \
                        address=getV('address'), username=getV('username'), password=getV('password'), \
                        email=getV('email'))
                if commit:
                    d.save()
        return d, err_msg



class PatientForm(HumanForm):
    relative = forms.CharField(label="Relative/Spouse", max_length=80, required=False)
    emergency_contact = forms.IntegerField(required=False)
    occupation = forms.CharField(max_length=40, required=False)

    def __str__(self):
        return 'Patient'

    def save(self, commit=True):
        def getV(field):
            return self[field].value()

        p = Patient(profile=getV('profile'), full_name=getV('full_name'), gender=getV('gender'), \
                dob=getV('dob'), phone_number=getV('phone_number'), address=getV('address'), \
                relative=getV('relative'), occupation=getV('occupation'), email=getV('email'), \
                emergency_contact=getV('emergency_contact'))
        if commit:
            p.save()
        return p, None


class CaseForm(forms.Form):
    disease = forms.ModelChoiceField(queryset=Disease.objects.all())
    patient = forms.ModelChoiceField(queryset=Patient.objects.all())
    doctors = forms.ModelChoiceField(queryset=Doctor.objects.all())
    s_date = forms.DateField(label="Start Date", widget = AdminDateWidget)
    e_date = forms.DateField(label="End Date", widget = AdminDateWidget)

    def __str__(self):
        return 'Case'


class ApptForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = []

    def __str__(self):
        return 'Appointment'
