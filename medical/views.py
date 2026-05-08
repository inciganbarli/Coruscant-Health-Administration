from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from .models import UserProfile, Patient, Doctor, DeviceData, MedicalReport, Order, OrderResult, EmergencyPatient
from .forms import (
    RegisterForm, PatientForm, DoctorForm, DeviceDataForm,
    MedicalReportForm, OrderForm, OrderResultForm, EmergencyPatientForm, OrderStatusForm
)
from django.http import FileResponse


def get_role(user):
    try:
        return user.userprofile.role
    except Exception:
        return None


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role=form.cleaned_data['role'])
            messages.success(request, 'Account created. Please login.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'medical/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'medical/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    role = get_role(request.user)
    context = {
        'role': role,
        'patient_count': Patient.objects.count(),
        'doctor_count': Doctor.objects.count(),
        'report_count': MedicalReport.objects.count(),
        'order_count': Order.objects.count(),
        'emergency_count': EmergencyPatient.objects.count(),
        'recent_patients': Patient.objects.all()[:5],
        'recent_reports': MedicalReport.objects.all()[:5],
        'pending_orders': Order.objects.filter(status='pending')[:5],
    }
    return render(request, 'medical/home.html', context)


# ── PATIENTS ────────────────────────────────────────────────

@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'medical/patient_list.html', {'patients': patients})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'medical/patient_detail.html', {
        'patient': patient,
        'reports': MedicalReport.objects.filter(patient=patient),
        'orders': Order.objects.filter(patient=patient),
        'device_data': DeviceData.objects.filter(patient=patient),
    })


@login_required
def patient_add(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient added.')
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'medical/patient_form.html', {'form': form, 'title': 'Add Patient', 'button_text': 'Add Patient'})


@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated.')
            return redirect('patient_detail', pk=pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'medical/patient_form.html', {'form': form, 'title': f'Edit: {patient.name}', 'button_text': 'Save Changes'})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted.')
        return redirect('patient_list')
    return render(request, 'medical/confirm_delete.html', {'object': patient, 'type': 'Patient', 'cancel_url': 'patient_list'})


# ── DOCTORS ────────────────────────────────────────────────

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'medical/doctor_list.html', {'doctors': doctors})


@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'medical/doctor_detail.html', {
        'doctor': doctor,
        'reports': MedicalReport.objects.filter(doctor=doctor),
        'orders': Order.objects.filter(doctor=doctor),
    })


@login_required
def doctor_add(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor added.')
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'medical/doctor_form.html', {'form': form, 'title': 'Add Doctor', 'button_text': 'Add Doctor'})


@login_required
def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated.')
            return redirect('doctor_detail', pk=pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'medical/doctor_form.html', {'form': form, 'title': f'Edit: {doctor.name}', 'button_text': 'Save Changes'})


@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor deleted.')
        return redirect('doctor_list')
    return render(request, 'medical/confirm_delete.html', {'object': doctor, 'type': 'Doctor', 'cancel_url': 'doctor_list'})


# ── DEVICE DATA ────────────────────────────────────────────

@login_required
def device_data_list(request):
    data = DeviceData.objects.all()
    return render(request, 'medical/device_data_list.html', {'data': data})


@login_required
def device_data_upload(request):
    if request.method == 'POST':
        form = DeviceDataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Device data uploaded.')
            return redirect('device_data_list')
    else:
        form = DeviceDataForm()
    return render(request, 'medical/device_data_form.html', {'form': form, 'title': 'Upload Device Data', 'button_text': 'Upload'})


@login_required
def device_data_delete(request, pk):
    item = get_object_or_404(DeviceData, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Deleted.')
        return redirect('device_data_list')
    return render(request, 'medical/confirm_delete.html', {'object': item, 'type': 'Device Data', 'cancel_url': 'device_data_list'})


# ── REPORTS ────────────────────────────────────────────────

@login_required
def report_list(request):
    reports = MedicalReport.objects.all()
    return render(request, 'medical/report_list.html', {'reports': reports})


@login_required
def report_detail(request, pk):
    report = get_object_or_404(MedicalReport, pk=pk)
    return render(request, 'medical/report_detail.html', {'report': report})


@login_required
def report_add(request):
    if request.method == 'POST':
        form = MedicalReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report created.')
            return redirect('report_list')
    else:
        form = MedicalReportForm()
    return render(request, 'medical/report_form.html', {'form': form, 'title': 'Create Medical Report', 'button_text': 'Create Report'})


@login_required
def report_edit(request, pk):
    report = get_object_or_404(MedicalReport, pk=pk)
    if request.method == 'POST':
        form = MedicalReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated.')
            return redirect('report_detail', pk=pk)
    else:
        form = MedicalReportForm(instance=report)
    return render(request, 'medical/report_form.html', {'form': form, 'title': 'Edit Report', 'button_text': 'Save Changes'})


@login_required
def report_delete(request, pk):
    report = get_object_or_404(MedicalReport, pk=pk)
    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted.')
        return redirect('report_list')
    return render(request, 'medical/confirm_delete.html', {'object': report, 'type': 'Medical Report', 'cancel_url': 'report_list'})


# ── ORDERS ────────────────────────────────────────────────

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'medical/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    result = getattr(order, 'result', None)
    status_form = OrderStatusForm(instance=order)
    if request.method == 'POST':
        status_form = OrderStatusForm(request.POST, instance=order)
        if status_form.is_valid():
            status_form.save()
            messages.success(request, 'Order status updated.')
            return redirect('order_detail', pk=pk)
    return render(request, 'medical/order_detail.html', {'order': order, 'result': result, 'status_form': status_form})


@login_required
def order_add(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order created.')
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'medical/order_form.html', {'form': form, 'title': 'Create Order', 'button_text': 'Create Order'})


@login_required
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated.')
            return redirect('order_detail', pk=pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'medical/order_form.html', {'form': form, 'title': 'Edit Order', 'button_text': 'Save Changes'})


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted.')
        return redirect('order_list')
    return render(request, 'medical/confirm_delete.html', {'object': order, 'type': 'Order', 'cancel_url': 'order_list'})


@login_required
def order_result_upload(request, pk):
    order = get_object_or_404(Order, pk=pk)
    existing = getattr(order, 'result', None)
    if request.method == 'POST':
        form = OrderResultForm(request.POST, request.FILES, instance=existing)
        if form.is_valid():
            result = form.save(commit=False)
            result.order = order
            result.save()
            order.status = 'completed'
            order.save()
            messages.success(request, 'Result uploaded.')
            return redirect('order_detail', pk=pk)
    else:
        form = OrderResultForm(instance=existing)
    return render(request, 'medical/order_result_form.html', {'form': form, 'order': order})


# ── EMERGENCY ────────────────────────────────────────────────

@login_required
def emergency_list(request):
    emergencies = EmergencyPatient.objects.all()
    return render(request, 'medical/emergency_list.html', {'emergencies': emergencies})


@login_required
def emergency_add(request):
    if request.method == 'POST':
        form = EmergencyPatientForm(request.POST)
        if form.is_valid():
            ep = form.save()
            patient = Patient.objects.create(
                name=ep.name,
                age=ep.age or 0,
                gender='O',
                phone=ep.contact_number,
                is_emergency=True,
            )
            ep.patient = patient
            ep.save()
            messages.success(request, f'Emergency patient "{ep.name}" admitted and registered.')
            return redirect('emergency_list')
    else:
        form = EmergencyPatientForm()
    return render(request, 'medical/emergency_form.html', {'form': form})


# ── ADMIN USER MANAGEMENT ────────────────────────────────────

@login_required
def user_management(request):
    if get_role(request.user) != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('home')
    users = User.objects.select_related('userprofile').all()
    return render(request, 'medical/user_management.html', {'users': users})


@login_required
def user_delete(request, pk):
    if get_role(request.user) != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('home')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted.')
        return redirect('user_management')
    return render(request, 'medical/confirm_delete.html', {'object': user, 'type': 'User', 'cancel_url': 'user_management'})


@login_required
def download_file(request, model_name, pk):
    """
    Securely serves encrypted files by decrypting them on-the-fly.
    Checks user roles to ensure they have permission to access the file.
    """
    if model_name == 'device':
        obj = get_object_or_404(DeviceData, pk=pk)
        file_field = obj.file
        patient = obj.patient
    elif model_name == 'result':
        obj = get_object_or_404(OrderResult, pk=pk)
        file_field = obj.result_file
        patient = obj.order.patient
    else:
        return HttpResponse("Invalid model type.", status=400)

    # Basic Permission Check
    role = get_role(request.user)
    if role == 'patient' and patient.user != request.user:
        messages.error(request, 'You do not have permission to download this file.')
        return redirect('home')

    # The custom storage.open() handles decryption
    try:
        response = FileResponse(file_field.open(), content_type='application/octet-stream')
        filename = file_field.name.split('/')[-1]
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        return HttpResponse(f"Error retrieving file: {str(e)}", status=500)
