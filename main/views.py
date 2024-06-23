from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient, Status, Appointment, Report, Feedback, TreatmentPlan, History,WoundHealing
from django.contrib.auth import update_session_auth_hash
# Create your views here.

def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user:
            auth_login(request, user)
            if Doctor.objects.filter(user=user).exists():
                request.session['name'] = Doctor.objects.get(user=user).name
                return redirect('doctor')
            else:
                request.session['name'] = Patient.objects.get(user=user).name
                return redirect('patient')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        phone = request.POST['phone']
        age = request.POST['age']
        user_type = request.POST['user_type']
        if password != password1:
            return render(request, 'signup.html', {'error': 'Password does not match'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})
        user = User.objects.create_user(username=email, email=email, password=password)
        if user_type == 'doctor':
            Doctor.objects.create(user=user, name=name, phone=phone, age=age)
        else:
            Patient.objects.create(user=user, name=name, phone=phone, age=age)
        return redirect('login')
    return render(request, 'signup.html',)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def passchange(request):
    user = request.user
    error = None
    if request.method == "POST":
        password = request.POST.get('password')
        npassword = request.POST.get('npassword')
        if not user.check_password(password):
            error = 'Invalid Password'
        elif password == npassword:
            error = 'New Password is the same as the old password'
        else:
            user.set_password(npassword)
            user.save()
            update_session_auth_hash(request, user)  
            return redirect('login')
    return render(request, 'updatePass.html', {
        'user': user,
        'error': error
    })
    

def doctor(request):
    return HttpResponse("Doctor Page")

def patient(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    historys = History.objects.filter(patient=patient)
    plans = TreatmentPlan.objects.all()
    return render(request, 'patient_dash.html', {'patient': patient, 'historys': historys, 'plans': plans})


def appointment(request, aptId):
    user = request.user
    try:
        treatment_plan = TreatmentPlan.objects.get(id=aptId)
    except TreatmentPlan.DoesNotExist:
        return HttpResponse("TreatmentPlan does not exist", status=404)

    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = Status.objects.get(id=1)
        
        appointment = Appointment.objects.create(
            doctor=treatment_plan.doctor, 
            status=status,
            patient=Patient.objects.get(user=user),
            date=date,
            time=time
        )
        return render(request, 'appointment.html', {'appointment': appointment})
    else:
        return render(request, 'appointment.html', {'treatment_plan': treatment_plan})


def health(request):
    if request.method == 'POST' and request.FILES.get('photos'):
        date = request.POST.get('date')
        description = request.POST.get('description')
        photos = request.FILES['photos']
        WoundHealing.objects.create(patient=request.user, date=date, description=description, photos=photos)

    return render(request, 'heal_wound.html')

def feedback(request):
    name = request.session.get('name')
    if request.method == 'POST':
        name = name
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Feedback.objects.create(name=name, email=email, subject=subject, message=message)
    return render(request, 'feedback.html', {'name': name})


# def report(request):
#     if request.method == 'POST' and request.FILES.get('report'):
#         patient = Patient.objects.get(user=request.user)
#         doctor = Doctor.objects.get(user=User.objects.get(
#             username=request.POST.get('doctor')))
#         report = request.FILES['report']
#         date = request.POST.get('date')
#         Report.objects.create(patient=patient, doctor=doctor, report=report, date=date)
#     return render(request, 'report.html')

@login_required
def report(request):
    patient = Patient.objects.get(user=request.user)
    reports = Report.objects.filter(patient=patient)
    
    return render(request, 'report.html', {'reports': reports})


