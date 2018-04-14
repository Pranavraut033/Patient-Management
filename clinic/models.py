import datetime
from django.db import models
from django.utils import timezone
from passlib.hash import pbkdf2_sha256
from . import *
from .utils import utilities as utils

def get_adv_date():
    return utils.get_adv_date(7)

def get_empty(arg):
    return eval(arg).create_empty()


class Human(models.Model):
    profile = models.ImageField(upload_to = 'clinic/profile_pictures/', \
            blank=True, default='clinic/profile_pictures/generic_profile.png')
    full_name = models.CharField(max_length=80)
    gender = models.CharField(choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ), \
                                max_length=1)
    phone_number = models.IntegerField()
    dob = models.DateField("Date of Birth")
    email = models.CharField(max_length=40, null=True, blank=True)
    address = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        self.full_name = utils.titlecase(self.full_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

class Doctor(Human):
    degree = models.CharField(max_length=80, blank=True, default='')
    username = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=250)
    custom_pbkdf2 = pbkdf2_sha256.using(rounds=2146)

    def __str__(self):
        return '%s (%s)' % (super().__str__(), self.degree) if self.degree else super().__str__()

    def verify_user_name(self, user_name):
        return self.user_name is user_name

    def verify_password(self, password):
        if password is None or password is '':
            return False
        return Doctor.custom_pbkdf2.verify(password, self.password)

    def save(self, *args, **kwargs):
        if(not '$pbkdf2-sha256$2146$' in self.password):
            self.password = Doctor.custom_pbkdf2.hash(self.password)
        self.degree = utils.titlecase(self.degree)
        self.username = self.username.replace(' ', '')
        super().save(*args, **kwargs)

class Patient(Human):
    relative = models.CharField("Relative/Spouse", max_length=80, null=True, blank=True)
    emergency_contact = models.IntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=40, null=True, blank=True)


class FromSys(models.Model):
    name = models.CharField("From System", max_length=40)

    def __str__(self):
        return self.name

    def create_empty():
        return FromSys.objects.get_or_create(name="Removed")


class Disease(models.Model):
    def e():
        return get_empty("FromSys")

    name = models.CharField(max_length=80)
    abrv = models.CharField("Abbreviation", max_length=15, primary_key=True)
    from_system = models.ForeignKey(FromSys, on_delete=models.SET(e))

    def __str__(self):
        return "%s (%s)" % (self.name, self.abrv) if self.abrv is not None else self.name

    def create_empty():
        return Disease.objects.get_or_create(name="Removed", abrv="rmd")


class Case(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctors = models.ManyToManyField(Doctor)

    s_date = models.DateField("Start Date")
    e_date = models.DateField("End Date", null=True, blank=True, default=None)

    def __str__(self):
        return "(%s : %s) - %s" % (str(self.patient), self.disease.name, \
                str([str(x) for x in self.doctors.all()]).replace("\'", ''))

    def is_closed(self):
        if(self.e_date is None):
            return False
        return self.e_date <= timezone.localdate()

    is_closed.admin_order_field = '-s_date'
    is_closed.boolean = True
    is_closed.short_description = 'Is case closed?'


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appt_time = models.DateTimeField("Appointment Time", default=utils.get_adv_date)

    place = models.CharField(choices=\
            (('C', 'Clinic'), ('MH', 'My House'), ('TH', 'Patient\'s House'), ('K', 'Custom')), \
            max_length=1, default='C')
    custom = models.CharField("Custom Location", max_length=80, blank=True, null=True)

    def __str__(self):
        return "%s:%s- %s" % (self.patient, self.doctor, str(self.appt_time))


class FollowUp(models.Model):
    fees = models.IntegerField("Payment", null=True)
    time = models.DateTimeField("Follow-Up Taken At", default=timezone.now)

    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "(%s : %s) - %s" % (str(self.case.patient), self.case.disease.name, str(self.doctor))

    def is_settled(self):
        return self.fees is not None

    def get_patient(self):
        return self.case.patient

    is_settled.admin_order_field = '-time'
    is_settled.boolean = True
    is_settled.short_description = 'Is settled?'
    get_patient.short_description = 'Patient'

class Complaint(models.Model):
    name = models.CharField("Complaint", max_length=120)
    effect = models.CharField("Effect", max_length=40)
    followUp = models.ForeignKey(FollowUp, on_delete=models.CASCADE)

    def __str__(self):
        return name + ": " + effect
