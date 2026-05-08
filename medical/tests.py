from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserProfile, Patient, Doctor, DeviceData, MedicalReport, Order, OrderResult, EmergencyPatient
import os
from django.conf import settings

class MedicalSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create an admin user
        self.admin_user = User.objects.create_superuser(username='admin', password='password', email='admin@test.com')
        UserProfile.objects.create(user=self.admin_user, role='admin')
        
        # Create a doctor user
        self.doctor_user = User.objects.create_user(username='doctor', password='password')
        UserProfile.objects.create(user=self.doctor_user, role='doctor')
        self.doctor_profile = Doctor.objects.create(user=self.doctor_user, name='Strangelove', specialization='General')
        
        # Create a patient user
        self.patient_user = User.objects.create_user(username='patient', password='password')
        UserProfile.objects.create(user=self.patient_user, role='patient')
        self.patient_profile = Patient.objects.create(user=self.patient_user, name='Skywalker', age=25, gender='M')

    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'email': 'new@test.com',
            'role': 'patient'
        })
        self.assertEqual(response.status_code, 302) # Redirect to login
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertEqual(user.userprofile.role, 'patient')

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'doctor',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302) # Redirect to home

    def test_patient_management(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('patient_add'), {
            'name': 'Han Solo',
            'age': 35,
            'gender': 'M',
            'blood_type': 'O+'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Patient.objects.filter(name='Han Solo').exists())

    def test_encryption_workflow(self):
        self.client.login(username='patient', password='password')
        test_content = b"Confidential Medical Data"
        test_file = SimpleUploadedFile("test_data.txt", test_content)
        
        # Upload device data
        response = self.client.post(reverse('device_data_upload'), {
            'patient': self.patient_profile.pk,
            'title': 'Heart Rate Logs',
            'file': test_file
        })
        self.assertEqual(response.status_code, 302)
        
        data_obj = DeviceData.objects.get(title='Heart Rate Logs')
        file_path = data_obj.file.path
        
        # Verify file on disk is encrypted (not equal to original content)
        with open(file_path, 'rb') as f:
            disk_content = f.read()
            self.assertNotEqual(disk_content, test_content)
        
        # Verify retrieval via download view is decrypted correctly
        response = self.client.get(reverse('download_file', args=['device', data_obj.pk]))
        self.assertEqual(response.status_code, 200)
        downloaded_content = b"".join(response.streaming_content)
        self.assertEqual(downloaded_content, test_content)

    def test_medical_report(self):
        self.client.login(username='doctor', password='password')
        response = self.client.post(reverse('report_add'), {
            'patient': self.patient_profile.pk,
            'doctor': self.doctor_profile.pk,
            'diagnosis': 'Brainworm Rot Type A',
            'treatment': 'Quarantine and Vaccination'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MedicalReport.objects.filter(diagnosis__contains='Brainworm').exists())

    def test_emergency_admission(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('emergency_add'), {
            'name': 'Unknown Pilot',
            'condition': 'Crushed by TIE Fighter'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(EmergencyPatient.objects.filter(name='Unknown Pilot').exists())
        self.assertTrue(Patient.objects.filter(name='Unknown Pilot', is_emergency=True).exists())

    def test_order_workflow(self):
        self.client.login(username='doctor', password='password')
        order = Order.objects.create(
            patient=self.patient_profile,
            doctor=self.doctor_profile,
            order_type='ct_scan',
            department='Radiology'
        )
        
        # Upload result
        test_file = SimpleUploadedFile("scan.jpg", b"fake-image-content")
        response = self.client.post(reverse('order_result_upload', args=[order.pk]), {
            'uploaded_by': 'Technician 7',
            'result_text': 'All clear',
            'result_file': test_file
        })
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')
        self.assertTrue(OrderResult.objects.filter(order=order).exists())
