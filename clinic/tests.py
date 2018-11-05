from django.test import TestCase
from django.utils import timezone
from clinic.models import Doctor, Patient, Disease, Case
import datetime
# Create your tests here.

def create_doctor(username, password):
    return Doctor.objects.create(full_name='doctor', gender='O', degree=' ', dob=timezone.now(), \
            phone_number=1234567890, address='abc', user_name=username, password=password)

def create_patient():
    return Patient.objects.create(full_name='patient', gender='O', dob=timezone.now(), \
            phone_number=1234567890, address='abc')

def create_case(d, p, days):
    return Case.objects.create(disease=Disease.objects.create(name='fever', abrv='fvr'), patient=p, \
            doctor=d, s_date=timezone.now() - datetime.timedelta(days=days))


class DoctorModelsTest(TestCase):
    def test_verify_user_name(self):
        d = create_doctor('pranav', 'password')
        self.assertIs(d.verify_user_name(None), False)
        self.assertIs(d.verify_user_name(''), False)
        self.assertIs(d.verify_user_name('Pranav'), False)
        self.assertIs(d.verify_user_name('pranav'), True)

    def test_verify_user_name(self):
        d = create_doctor('pranav', 'password')
        self.assertIs(d.verify_password(None), False)
        self.assertIs(d.verify_password(''), False)
        self.assertIs(d.verify_password('Password'), False)
        self.assertIs(d.verify_password('password'), True)

def get_all():
    p = create_patient()
    d = create_doctor('pranav', 'passsword')
    return d, p, create_case(p=p, d=d, days=-2)


class PatientModelsTest(TestCase):
    def test_is_closed(self):
        d, p, c = get_all()
        # if e_date is null
        self.assertIs(c.is_closed(), False)
        # future date
        c.e_date = timezone.localdate() + datetime.timedelta(days=20)
        c.save()
        self.assertIs(c.is_closed(), False)

        c.e_date = timezone.localdate() - datetime.timedelta(days=2)
        c.save()

        self.assertIs(c.is_closed(), True)
