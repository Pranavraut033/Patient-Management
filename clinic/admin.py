from django.contrib import admin
from .models import *


class CasesInLine(admin.TabularInline):
    model = Case
    extra = 1


class AppointmentCasesInLine(admin.TabularInline):
    model = Appointment
    extra = 1


class ComplaintInLine(admin.TabularInline):
    model = Complaint
    extra = 5


class DoctorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Login information', {'fields': ['username', 'password']}),
        ('Personal information', {'fields': ['profile', 'full_name', 'gender', 'dob']}),
        ('Extra information', {'fields': ['phone_number', 'email', 'degree', 'address']}),
    ]
    inlines = [AppointmentCasesInLine]
    list_display = ('full_name', 'phone_number', 'email', 'degree', )


class PatientAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal information', {'fields': ['profile','full_name', 'gender', 'dob']}),
        ('Emergency information', {'fields': ['relative', 'emergency_contact']}),
        ('Extra information', {'fields': ['phone_number', 'email', 'address']}),
    ]
    inlines = [CasesInLine]
    list_display = ('full_name', 'phone_number', 'email',)


class CaseAdmin(admin.ModelAdmin):
    list_display = ('patient', '__str__', 's_date', 'e_date', 'is_closed',)


class FollowUpAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ('Personal information', {'fields': ['profile','full_name', 'gender', 'dob']}),
    #     ('Emergency information', {'fields': ['relative', 'emergency_contact']}),
    #     ('Extra information', {'fields': ['phone_number', 'email', 'address']}),
    # ]
    inlines = [ComplaintInLine]
    list_display = ('get_patient', 'case', "time", 'is_settled', )

admin.site.register(Disease)
admin.site.register(Appointment)
admin.site.register(FromSys)
admin.site.register(Case, CaseAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(FollowUp, FollowUpAdmin)
