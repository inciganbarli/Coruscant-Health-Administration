from django.db import models
from django.contrib.auth.models import User
from .storage import EncryptedFileSystemStorage

encrypted_storage = EncryptedFileSystemStorage()


class UserProfile(models.Model):
    ROLES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Administrator'),
        ('emergency', 'Emergency Services'),
        ('department', 'Department'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Patient(models.Model):
    GENDER = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='patient_profile')
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    date_admitted = models.DateField(auto_now_add=True)
    is_emergency = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_profile')
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    department = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name}"

    class Meta:
        ordering = ['name']


class DeviceData(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='device_data')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='device_data/', storage=encrypted_storage)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.title}"

    class Meta:
        ordering = ['-uploaded_at']


class MedicalReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report: {self.patient.name} — {self.doctor.name}"

    class Meta:
        ordering = ['-date_created']


class Order(models.Model):
    ORDER_TYPES = [
        ('ct_scan', 'CT Scan'),
        ('mri', 'MRI'),
        ('xray', 'X-Ray'),
        ('blood_test', 'Blood Test'),
        ('ultrasound', 'Ultrasound'),
        ('ecg', 'ECG'),
        ('other', 'Other'),
    ]
    STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES)
    department = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_order_type_display()} for {self.patient.name}"

    class Meta:
        ordering = ['-date_created']


class OrderResult(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='result')
    result_text = models.TextField(blank=True)
    result_file = models.FileField(upload_to='order_results/', blank=True, storage=encrypted_storage)
    uploaded_by = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.order}"


class EmergencyPatient(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(null=True, blank=True)
    condition = models.TextField()
    contact_number = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    arrived_at = models.DateTimeField(auto_now_add=True)
    patient = models.OneToOneField(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_record')

    def __str__(self):
        return f"Emergency: {self.name}"

    class Meta:
        ordering = ['-arrived_at']
