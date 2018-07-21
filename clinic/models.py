import datetime
from django.db import models
from django.utils import timezone
from passlib.hash import pbkdf2_sha256
from .utils import utilities as utils
from .utils.contants import *

specialties = (('ped', 'Pediatrics'), ('cardio','Cardiologist'), ('gyno', 'Gynaecolgist'), ('neuro','Neurologist'), ('onco','Oncologist'), \
               ('phy', 'Physician'), ('ns', 'Neuro Surgeon'), ('gs', 'General Surgeon'), ('gp', 'General Practitioner'), )
bld_grps=((0, 'A+'), (1, 'B+'), (2, 'AB+'), (3, 'O+'), (4, 'A-'), (5, 'B-'), (6, 'AB-'), (7, 'O-'))

def get_adv_date():
    return utils.get_adv_date(7)

def get_empty(arg):
    return eval(arg).create_empty()


class Symptom(models.Model):
    name = models.CharField(max_length=40)
    disp = models.CharField(max_length=120, null=True, blank=True)


class Medicine(models.Model):
    name = models.CharField(max_length=40)
    abbrv = models.CharField(max_length=10, unique=True)
    disp = models.CharField(max_length=120, null=True,blank=True)


class Disease(models.Model):
    scientific_name = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    symptoms = models.ManyToManyField(Symptom)
    prescriptions = models.ManyToManyField(Medicine)


class Human(models.Model):
    profile = models.ImageField(upload_to = 'clinic/profile_pictures/', blank=True, default='clinic/profile_pictures/generic_profile.png')
    reg_time = models.DateTimeField("Registration Time", auto_now_add=True)

    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    
    gender = models.CharField(choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ), max_length=1)
    phone_number = models.BigIntegerField()
    dob = models.DateField('Date of Birth')
    email = models.CharField('Email Address', max_length=40, blank=True)
    bld_grp = models.SmallIntegerField("Blood Group", choices=bld_grps)

    s_address = models.CharField("Street Address", max_length=100)
    city = models.CharField(max_length=40, blank=True)
    state = models.CharField(choices=states, max_length=2)
    country = models.CharField(choices=countries, max_length=2) 
    pincode = models.IntegerField()

    def name(self):
        return self.first_name + " " + self.last_name
    
    def save(self, *args, **kwargs):
        self.first_name = utils.titlecase(self.first_name)
        self.middle_name = utils.titlecase(self.middle_name)
        self.last_name = utils.titlecase(self.last_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name()


class Doctor(Human):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=100)
    
    speciality  = models.CharField('Medical specialties', choices=specialties, max_length=3, default='gp')
    qual = models.CharField('Qualification', max_length=20, default='', blank=True)
    bio = models.CharField('Biography', max_length=120, blank=True)  

    custom_pbkdf2 = pbkdf2_sha256.using(rounds=2146)

    def __str__(self):
        return '%s (%s)' % (super().__str__(), self.qual) if self.qual else super().__str__()

    def verify_user_name(self, user_name):
        return self.user_name is user_name

    def verify_password(self, password):
        if password is None or password is '':
            return False
        return Doctor.custom_pbkdf2.verify(password, self.password)

    def save(self, *args, **kwargs):
        if(not '$pbkdf2-sha256$2146$' in self.password):
            self.password = Doctor.custom_pbkdf2.hash(self.password)
        self.qual = utils.titlecase(self.qual)
        self.username = self.username.replace(' ', '')
        super().save(*args, **kwargs)


class Patient(Human):
    er_cont_name = models.CharField('Emergency Contact Name', max_length=50, blank=True)
    relation = models.CharField("Relation with the contact", max_length=10, blank=True)
    emergency_contact = models.BigIntegerField(blank=True)
    
    occupation = models.CharField(max_length=40, null=True, blank=True)
    med_info = models.CharField('Medical Information', max_length=100, blank=True)


class Case(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    reg_time = models.DateField('Initial vist', default=timezone.now)
    l_visit = models.DateField('Last vist', null=True, blank=True, default=None)

    def __str__(self):
        return "(%s : %s) - %s" % (str(self.patient), self.disease.name, str([str(x) for x in self.doctors.all()]).replace("\'", ''))

    def is_closed(self):
        if(self.l_visit is None):
            return False
        return self.l_visit <= timezone.now()

    is_closed.admin_order_field = '-reg_time'
    is_closed.boolean = True
    is_closed.short_description = 'Is case closed?'
    

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.PROTECT)
    time = models.DateTimeField("Appointment Time", default=utils.get_adv_date)
    loc = models.CharField('Location', choices=(('C', 'Clinic'), ('h', 'House Vist'), ('v', 'Visting'), ('ct', 'Custom')), max_length=1, default='C')
    cus = models.CharField("Custom Location", max_length=80, blank=True, null=True)

    def __str__(self):
        return "%s:%s- %s" % (self.patient, self.doctor, str(self.time))


class FollowUp(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=50)
    symptoms = models.ManyToManyField(Symptom)
    prescriptions = models.ManyToManyField(Medicine)
    pat_comp = models.CharField('Pratient\'s Complaint', max_length=100, null=True, blank=True)
    note = models.CharField(max_length=100, null=True, blank=True)
    
    fee = models.PositiveSmallIntegerField(blank=True, default=100)
    gift = models.BooleanField(default=False)
    time = models.DateTimeField('Follow-Up Time', default=timezone.now)
    
    def __str__(self):
        return "(%s : %s) - %s" % (str(self.case.patient), self.case.disease.name, str(self.doctor))

    def is_settled(self):
        return self.gift and bool(self.fees)

    def get_patient(self):
        return self.case.patient

    is_settled.admin_order_field = '-time'
    is_settled.boolean = True
    is_settled.short_description = 'Is settled?'
    get_patient.short_description = 'Patient'


    
