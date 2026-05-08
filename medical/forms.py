from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Patient, Doctor, DeviceData, MedicalReport, Order, OrderResult, EmergencyPatient

W = {'class': 'form-control'}
WT = {'class': 'form-control', 'rows': 3}


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs=W))
    role = forms.ChoiceField(choices=UserProfile.ROLES, widget=forms.Select(attrs=W))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'phone', 'address', 'blood_type']
        widgets = {
            'name': forms.TextInput(attrs={**W, 'placeholder': 'Full name'}),
            'age': forms.NumberInput(attrs={**W, 'placeholder': 'Age'}),
            'gender': forms.Select(attrs=W),
            'phone': forms.TextInput(attrs={**W, 'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={**WT, 'placeholder': 'Address'}),
            'blood_type': forms.TextInput(attrs={**W, 'placeholder': 'e.g. A+, O-'}),
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'department', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={**W, 'placeholder': 'Full name'}),
            'specialization': forms.TextInput(attrs={**W, 'placeholder': 'e.g. Cardiologist'}),
            'department': forms.TextInput(attrs={**W, 'placeholder': 'e.g. Cardiology'}),
            'phone': forms.TextInput(attrs={**W, 'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={**W, 'placeholder': 'Email'}),
        }


class DeviceDataForm(forms.ModelForm):
    class Meta:
        model = DeviceData
        fields = ['patient', 'title', 'description', 'file']
        widgets = {
            'patient': forms.Select(attrs=W),
            'title': forms.TextInput(attrs={**W, 'placeholder': 'e.g. Heart Rate Monitor Data'}),
            'description': forms.Textarea(attrs={**WT, 'placeholder': 'Description (optional)'}),
        }


class MedicalReportForm(forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = ['patient', 'doctor', 'diagnosis', 'treatment', 'notes']
        widgets = {
            'patient': forms.Select(attrs=W),
            'doctor': forms.Select(attrs=W),
            'diagnosis': forms.Textarea(attrs={**WT, 'placeholder': 'Diagnosis...'}),
            'treatment': forms.Textarea(attrs={**WT, 'placeholder': 'Treatment plan...'}),
            'notes': forms.Textarea(attrs={**WT, 'placeholder': 'Extra notes (optional)'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['patient', 'doctor', 'order_type', 'department', 'notes']
        widgets = {
            'patient': forms.Select(attrs=W),
            'doctor': forms.Select(attrs=W),
            'order_type': forms.Select(attrs=W),
            'department': forms.TextInput(attrs={**W, 'placeholder': 'e.g. Radiology'}),
            'notes': forms.Textarea(attrs={**WT, 'placeholder': 'Notes for the department...'}),
        }


class OrderResultForm(forms.ModelForm):
    class Meta:
        model = OrderResult
        fields = ['result_text', 'result_file', 'uploaded_by']
        widgets = {
            'result_text': forms.Textarea(attrs={**WT, 'placeholder': 'Result findings...'}),
            'uploaded_by': forms.TextInput(attrs={**W, 'placeholder': 'Your name / department'}),
        }


class EmergencyPatientForm(forms.ModelForm):
    class Meta:
        model = EmergencyPatient
        fields = ['name', 'age', 'condition', 'contact_number', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={**W, 'placeholder': 'Patient name'}),
            'age': forms.NumberInput(attrs={**W, 'placeholder': 'Age (if known)'}),
            'condition': forms.Textarea(attrs={**WT, 'placeholder': 'Emergency condition description...'}),
            'contact_number': forms.TextInput(attrs={**W, 'placeholder': 'Emergency contact'}),
            'notes': forms.Textarea(attrs={**WT, 'placeholder': 'Additional notes'}),
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {'status': forms.Select(attrs=W)}
