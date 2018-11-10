from django import forms

from clinic.models import *
from clinic.utils.log import Logger

import clinic.utils.validators as v

logger = Logger()

class LoginForm(forms.Form):
	username = forms.CharField(validators=[v.validate_username_login])
	password = forms.CharField()

	def clean(self):
		cleaned_data = super().clean()
		username = cleaned_data.get('username')
		password = cleaned_data.get('password')
		if (username):
			d = Doctor.objects.get(pk=username)
			# Checking Password
			if not d.verify_password(password):
				self.add_error('password', 'Wrong password!')
		return cleaned_data

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = '__all__'

class PhoneForm(forms.ModelForm):
	class Meta:
		model = Phone
		fields = '__all__'

class PatientForm(forms.ModelForm):
	class Meta:
		model = Patient
		exclude = ['reg_time', 'clinic', ]

class EmergencyContactForm(forms.ModelForm):
	class Meta:
		model = EmergencyContact
		exclude = ['person', ]


class PatientFormSet:

	def __init__(self, data={}, clinic=None):
		self.data = data
		self.clinic = clinic
		logger.d("data:", data)
		if not isinstance(data, dict):
			raise Exception("Data should be of type dictonary and not" + str(type(data)))
		self.patient = PatientForm(data)
		self.address = AddressForm(data)
		self.emergency_contact = EmergencyContactForm(data)
		self.er_phones = [PhoneForm({'phone_number' : data['er_phone_number'], 'type': ['er_type']} if 'er_phone_number' in data else data), ]
		self.phones = [PhoneForm(data), ]
		if data:
			i = 1
			while 'phone_number-' + str(i) in data:
				phone_number = data['phone_number-' + str(i)]
				type = data['type-' + str(i)]
				p = PhoneForm({'phone_number' : phone_number, 'type' : type, })
				self.phones.append(p)
				i = i + 1
				er_phones =[]
			i = 0
			while 'er_phone_number-' + str(i) in data:
				phone_number = data['er_phone_number-' + str(i)]
				type = data['er_type-' + str(i)]
				p = PhoneForm({'phone_number': phone_number, 'type': type, })
				p.index = i
				self.er_phones.append(p)
				i = i + 1

	def get_fields(self):
		return [self.patient, self.address, self.phones, self.emergency_contact, self.er_phones];

	def get_models_all(self):
		return [self.patient, self.address, self.emergency_contact, ] + self.phones #+ self.er_phones

	def is_valid(self):
		b = True;
		for form in self.get_models_all():
			b = b and form.is_valid()
			if not b: return b
		return b

	def get_form_as_p(self):
		return "".join([form.as_p() for form in self.get_models_all()])

	def get_form_as_table(self):
		return "".join([form.as_table() for form in self.get_models_all()])

	def get_form_as_li(self):
		return "".join([form.as_li() for form in self.get_models_all()])

	def get_errors(self):
		l = [form.errors for form in self.get_models_all() if not form.is_valid()]
		logger.d(l)
		er = {}
		for i in l:
			er = {**er, **i}
		return er

	def save(self):
		if not self.is_valid():
			raise Exception("Form is not valid!\n" + self.get_errors())
		patient = self.patient.save(commit=False)
		patient.clinic = self.clinic
		patient.save()
		person = patient.person_ptr
		address = self.address.save()
		er_cont =  self.emergency_contact.save(commit=False)
		er_cont.person = person
		er_cont.save()
		d = PersonAddress(person=person, address=address).save();
		# logger.d("PersonAddress:", d, "Address:",address)

		for phone in self.phones:
			phone = phone.save()
			PersonPhone(person=patient.person_ptr, phone_number=phone).save()

		for er_phone in self.er_phones:
			phone = er_phone.save()
			EmergencyContactPhone(er_phone_number=phone, emergency_contact=er_cont).save()
		return patient

	def __str__(self):
		return self.get_form_as_p()

# from django.forms.models import formset_factory, inlineformset_factory, BaseInlineFormSet
# from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.admin.widgets import AdminDateWidget, ForeignKeyRawIdWidget
# from django.core.exceptions import ObjectDoesNotExist
# from django.db.models.fields.reverse_related import ManyToOneRel
# from django.db.models.fields.related import OneToOneField
# from django.db.models.fields import AutoField
# import clinic.utils.constants as consts

# P_PhoneFormSet = inlineformset_factory(PersonPhone, Phone, fields='__all__', extra=1)
# P_AddressFormSet = inlineformset_factory(PersonAddress, Address, fields='__all__', extra = 1)
#
# class BasePersonPhoneFormSet(BaseInlineFormSet):
#
# 	def add_fields(self, form, index):
# 		super(BasePersonPhoneFormSet, self).add_fields(form, index)
#
# 		form.nested = P_PhoneFormSet(
# 						instance=form.instance,
# 						data=form.data if form.is_bound else None,
# 						files=form.files if form.is_bound else None,
# 						prefix='Phone-%s-%s' % (form.prefix, P_PhoneFormSet.get_default_prefix()),
# 						extra=1)
#
#
# class BasePersonAddressFormSet(BaseInlineFormSet):
#
# 	def add_fields(self, form, index):
# 		super(BasePersonAddressFormSet, self).add_fields(form, index)
#
# 		form.nested = P_AddressFormSet(
# 						instance=form.instance,
# 						data=form.data if form.is_bound else None,
# 						files=form.files if form.is_bound else None,
# 						prefix='Address-%s-%s' % (form.prefix, P_AddressFormSet.get_default_prefix()),
# 						extra=1)
#
# PersonPhoneFormSet = inlineformset_factory(Person, PersonPhone, fields='__all__', \
# 											 formset=BasePersonPhoneFormSet, extra=1)
#
# PersonAddressFormSet = inlineformset_factory(Person, PersonAddress, fields='__all__', \
# 											 formset=BasePersonAddressFormSet, extra=1)

# class PersonForm(SuperModelForm):
# 	phone = ModelFormField(form_class=PersonPhoneForm)
# 	address = ModelFormField(form_class=PersonAddressForm)
#
# 	class Meta:
# 		model = Person
# 		exclude = ['id', 'reg_time']
#
# class PatientForm(SuperModelForm):
# 	phone = InlineFormSetField(formset_class=PersonPhoneFormSet)
# 	address = InlineFormSetField(formset_class=PersonAddressFormSet)
#
# 	def __init__(self, clinic=None, *arg, **kwargs):
# 		super().__init__(*arg, **kwargs)
# 		self.clinic = clinic
#
# 	class Meta:
# 		model = Patient
# 		exclude = ['id', 'reg_time', 'clinic']


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
#     qual = forms.CharField(label='Qualification', max_length=20, required=False)
#     bio = forms.CharField(label='Biography', required=False)
#
#     def __str__(self):
#         return getValue(self, 'username')
#
#     def save(self, commit=True):
#         if not self.is_valid():
#             raise Exception('The form has invalid fields' + str(self.errors))
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
#         return getValue(self, 'first_name') + getValue(self, 'last_name')
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
