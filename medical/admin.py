from django.contrib import admin
from .models import UserProfile, Patient, Doctor, DeviceData, MedicalReport, Order, OrderResult, EmergencyPatient


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'blood_type', 'phone', 'is_emergency', 'date_admitted']
    search_fields = ['name', 'phone']
    list_filter = ['gender', 'is_emergency', 'date_admitted']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'department', 'phone', 'email', 'date_joined']
    search_fields = ['name', 'specialization', 'department']
    list_filter = ['specialization']


@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ['patient', 'title', 'uploaded_at']
    search_fields = ['patient__name', 'title']


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date_created']
    search_fields = ['patient__name', 'doctor__name', 'diagnosis']
    list_filter = ['date_created', 'doctor']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'order_type', 'department', 'status', 'date_created']
    search_fields = ['patient__name', 'doctor__name', 'department']
    list_filter = ['order_type', 'status', 'date_created']


@admin.register(OrderResult)
class OrderResultAdmin(admin.ModelAdmin):
    list_display = ['order', 'uploaded_by', 'uploaded_at']


@admin.register(EmergencyPatient)
class EmergencyPatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'condition', 'contact_number', 'arrived_at']
    search_fields = ['name', 'contact_number']
