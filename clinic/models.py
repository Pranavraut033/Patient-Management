import os, datetime

from django.db import models
from django.utils import timezone
from passlib.hash import pbkdf2_sha256

import clinic.utils.utilities as utils
import clinic.utils.constants as consts
import clinic.utils.validators as v
from clinic.utils.log import Logger
# NOTE: ADD ManyToManyField, ForeignKey Field first before adding parent in the database
logger = Logger()
def get_adv_date():
	return utils.get_adv_date(7)

# def get_empty(arg):
#     return eval(arg).create_empty()

class Phone(models.Model):
	phone_number = models.BigIntegerField(validators=[v.validate_number])
	type = models.CharField(choices=consts.phone_type, max_length=1, default='h')

	def __str__(self):
		return str(self.phone_number) + ' (' + self.get_type_display()+ ')'

class Address(models.Model):
	s_address = models.CharField('Street Address', max_length=100)
	city = models.CharField(max_length=40, blank=True)
	state = models.CharField(choices=consts.states, max_length=2)
	country = models.CharField(choices=consts.countries, max_length=2)
	pincode = models.IntegerField(blank=False);

	def __str__(self):
		return self.s_address + ' (' + str(self.pincode) + ')'

class Disease(models.Model):
	name = models.CharField(max_length=40, primary_key=True)
	scientific_name = models.CharField(max_length=40, blank=True);
	description = models.CharField(max_length=100)

class Drug(models.Model):
	name = models.CharField(max_length=40, primary_key=True)
	abbreviation = models.CharField(max_length=10, unique=True)
	description = models.CharField(max_length=120, blank=True)
'''
	---		person		---
'''
def user_profile_directory(instance, filename):
	ext = os.path.splitext(filename)[1]
	return 'clinic/static/clinic/user_profile/%s-%s%s' % (instance.first_name, timezone.now().timestamp(), ext)

class Person(models.Model):
	profile = models.ImageField(upload_to=user_profile_directory, default='clinic/static/clinic/user_profile/no-profile.png')
	reg_time = models.DateTimeField('Registration Time', auto_now_add=True)

	first_name = models.CharField(max_length=20)
	middle_name = models.CharField(max_length=20, blank=True)
	last_name = models.CharField(max_length=20)

	gender = models.CharField(choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ), max_length=1)
	dob = models.DateField('Date of Birth')
	blood_type = models.PositiveSmallIntegerField(choices=consts.blood_groups, blank=True)
	bio = models.CharField('Biography', max_length=250, blank=True)

	email = models.CharField('Email Address', max_length=40, blank=True, validators=[v.validate_email])

	def full_name(self):
		return self.first_name + ' ' + self.middle_name + ' ' + self.last_name

	def name(self):
		return {'first_name' : self.first_name, 'middle_name' : self.middle_name, 'last_name' : self.last_name,}

	def dict_emergency_contact(self):
		return self.emergency_contact.dict()

	def age(self):
		return utils.getAge(self.dob)

	def get_profile_url(self):
		try:
			return utils.getimage(self.profile)
		except Exception as ex:
			print(ex)
			return 'clinic/user_profile/no-profile.png'

	def save(self, *args, **kwargs):
		for i in [self.first_name, self.middle_name, self.last_name]:
			i = utils.titlecase(i)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.first_name + ' ' + self.last_name

class PersonPhone(models.Model):
	person = models.OneToOneField(Person, null=True, on_delete=models.CASCADE)
	phone_number = models.OneToOneField(Phone, null=True, on_delete=models.CASCADE)

class PersonAddress(models.Model):
	address = models.OneToOneField(Address, null=True, on_delete=models.CASCADE)
	person = models.OneToOneField(Person, null=True, on_delete=models.CASCADE)

class EmergencyContact(models.Model):
	person = models.OneToOneField(Person, null=True, on_delete=models.SET_NULL)
	er_cont_name = models.CharField('Emergency Contact Name', max_length=50, blank=True)
	er_rel = models.CharField('Relationship with the Emergency contact', max_length=1, \
							   choices=(('S', 'Sprouse'), ('P', 'Parent'), ('s', 'Sibling'), \
									 	('G', 'Guardian'), ('O', 'Other'), ))

	def dict(self):
		return {'name' : self.er_cont_name, 'number' : er_number, 'relationship' : er_rel, }

class EmergencyContactPhone(models.Model):
	emergency_contact = models.OneToOneField(EmergencyContact, null=True, on_delete=models.CASCADE)
	er_phone_number = models.OneToOneField(Phone, null=True, on_delete=models.CASCADE)
'''
	---		end		---

	---		doctor	---
'''
class Doctor(Person):
	custom_pbkdf2 = pbkdf2_sha256.using(rounds=2146)

	username = models.CharField(max_length=20, primary_key=True, validators=[v.validate_username])
	password = models.CharField(max_length=100, validators=[v.validate_password])
	speciality  = models.CharField('Practitioner type', choices=consts.specialties, max_length=3,)
	qual = models.CharField('Qualification', max_length=20, blank=True)

	def __str__(self):
		return '%s (%s)' % (super().__str__(), self.qual) if self.qual else super().__str__()

	def verify_user_name(self, user_name):
		return self.user_name is user_name

	def verify_password(self, password):
		if not password: return False
		return self.custom_pbkdf2.verify(password, self.password)

	def save(self, *args, **kwargs):
		if(not '$pbkdf2-sha256$2146$' in self.password):
			self.password = Doctor.custom_pbkdf2.hash(self.password)
		self.qual = utils.titlecase(self.qual)
		self.username = self.username.replace(' ', '_')
		super().save(*args, **kwargs)
'''
	---			end			---

	---		other people	---
'''
'''
	---		clinic		---
'''
class Clinic(models.Model):
	clinic_head = models.OneToOneField(Doctor, on_delete=models.CASCADE)
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class Patient(Person):
	occupation = models.CharField(max_length=40, blank=True)
	med_info = models.CharField('Medical Information', max_length=100, blank=True)
	clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True)

class ClinicPhone(models.Model):
	clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
	phone_number = models.OneToOneField(Phone, null=True, on_delete=models.SET_NULL)

class Branch(models.Model):
	clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
	branch_head = models.OneToOneField(Doctor, on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	doe = models.DateField('Date of Establishment')
	type = models.CharField(choices=consts.clinic_type, max_length=2)

	def __str__(self):
		return "%s, %s (%s) - %s" % (self.clinic.name, self.name, self.get_type_display(), self.doe)

class BranchAssistantDoctor(models.Model):
	doctor = models.OneToOneField(Doctor, on_delete=models.SET_NULL, null=True)
	branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
	salary = models.IntegerField()

class BranchEmployee(models.Model):
	person = models.OneToOneField(Person, on_delete=models.SET_NULL, null=True)
	branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
	qual = models.CharField('Qualification', max_length=20, blank=True)
	salary = models.IntegerField()
	role = models.CharField(max_length=20);
	# TODO: ADD ROLE ENUM

class BranchAddress(models.Model):
	Branch = models.OneToOneField(Branch, on_delete=models.CASCADE)
	address = models.OneToOneField(Address, null=True, on_delete=models.SET_NULL)

class BranchPhone(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
	phone_number = models.OneToOneField(Phone, null=True, on_delete=models.SET_NULL)

class BranchTimming(models.Model):
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
	start = models.TimeField('Opens at')
	end = models.TimeField('Closes at')
	day = models.CharField(choices=consts.weekdays, max_length=3)
'''
	---		end		---

	---		case	---
'''
class Case(models.Model):
	title = models.CharField(max_length=50)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	date = models.DateTimeField('Registration date', default=timezone.now)
	refer = models.CharField(max_length=180, blank=True)

	def __str__(self):
	    return '%s - %s (%s)' % (self.title, self.patient, self.date.date())

class CaseDisease(models.Model):
	case = models.ForeignKey(Case, on_delete=models.CASCADE)
	disease = models.OneToOneField(Disease, on_delete=models.CASCADE)

def report_directory(instance, filename):
	ext = os.path.splitext(filename)[1]
	return 'clinic/static/clinic/reports/%s%s.%s' % (instance.case.title, instance.title + ext)

class CaseReport(models.Model):
	case = models.ForeignKey(Case, on_delete=models.CASCADE)
	title = models.CharField(max_length=80)
	key_read = models.CharField("Key Reading", max_length=50, blank=True)
	photo = models.ImageField(upload_to=report_directory, blank=True)
'''
	---     Visit    ---
'''
class CaseVisit(models.Model):
	case = models.ForeignKey(Case, on_delete=models.CASCADE)
	time = models.DateTimeField('Visit Time', default=timezone.now)
	fees = models.PositiveSmallIntegerField(default=100)
	notes = models.CharField(max_length=200, blank=True)

class VisitDrug(models.Model):
	visit = models.ForeignKey(CaseVisit, on_delete=models.CASCADE)
	drug = models.OneToOneField(Drug, on_delete=models.CASCADE)
	dose = models.CharField(max_length=10)

class VisitExamination(models.Model):
	visit = models.ForeignKey(CaseVisit, on_delete=models.CASCADE)
	about = models.CharField(max_length=25)
	read = models.CharField('Reading', max_length=10)

class VisitComplaint(models.Model):
	visit = models.ForeignKey(CaseVisit, on_delete=models.CASCADE);
	complaint = models.CharField(max_length=40)
	description = models.CharField(max_length=120, blank=True)
	status = models.CharField(max_length=30)

	def __str__(self):
		return self.complaint + ' ' + self.status
'''
	---		end		---
'''
class CaseAppointment(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	case = models.ForeignKey(Case, on_delete=models.PROTECT)

	time = models.DateTimeField('Appointment Time', default=utils.get_adv_date)
	location = models.CharField('Location', choices=consts.custom_location, max_length=1, default='C')
	custom_location = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return '(%s : %s) @ %s at %s' % (self.patient, self.doctor, self.get_location_display() if self.location != 'c'
		 														else self.custom_location, self.time.time())
'''
	---		case_end	---
'''

# TODO: Complete This
# class Event(models.Model):
#     pk = models.CharField(max_length=20)
#     model_altered = models.CharField(max_length=20)
