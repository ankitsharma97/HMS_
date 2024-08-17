from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import patient_required
from .models import Doctor, Patient, Status, Appointment, Report, Feedback, TreatmentPlan, History,WoundHealing,Polls,Answer
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
        if password != password1:
            return render(request, 'signup.html', {'error': 'Password does not match'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})
        user = User.objects.create_user(username=email, email=email, password=password)

        Patient.objects.create(user=user, name=name, phone=phone, age=age)
        return redirect('login')
    return render(request, 'signup.html',)

@patient_required
def logout(request):
    auth_logout(request)
    return redirect('home')

@patient_required
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
    
@patient_required
def doctor(request):
    return HttpResponse("Doctor Page")

@patient_required
def patient(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    historys = History.objects.filter(patient=patient)
    plans = TreatmentPlan.objects.all()
    return render(request, 'patient_dash.html', {'patient': patient, 'historys': historys, 'plans': plans})

@patient_required
def editprofile(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        pin_code = request.POST.get('pin_code')
        patient.name = name
        patient.phone = phone
        patient.age = age
        patient.mobile_number = mobile_number
        patient.address = address
        patient.pin_code = pin_code
        patient.save()
        return redirect('patient')
    return render(request, 'editprofile.html', {'patient': patient})

@patient_required
def viewappointments(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    appointments = Appointment.objects.filter(patient=patient)
    
    return render(request, 'viewappointment.html', {'appointments': appointments})

@patient_required
def appointment(request, aptId):
    user = request.user
    if aptId==9999:
        doctors = Doctor.objects.all()
    else:
        try:
            treatment_plan = TreatmentPlan.objects.get(id=aptId)
            doctors = treatment_plan.doctor
        except TreatmentPlan.DoesNotExist:
            return HttpResponse("TreatmentPlan does not exist", status=404)
    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        docId = request.POST.get('doctor')
        doctor = Doctor.objects.get(id=docId)
        status = Status.objects.get(id=1)
        
        appointment = Appointment.objects.create(
            doctor=doctor, 
            status=status,
            patient=Patient.objects.get(user=user),
            date=date,
            time=time
        )
        return redirect('viewappointments')
    else:
        return render(request, 'appointment.html', { 'doctors': doctors})

@patient_required
def deleteappointment(request, aptId):
    Appointment.objects.get(id=aptId).delete()
    return redirect('viewappointments')

@patient_required
def  plans(request):
    user = request.user
    treatments = TreatmentPlan.objects.all()
    return render(request, 'viewtreatments.html', {'treatments': treatments})
    
@patient_required
def health(request):
    if request.method == 'POST' and request.FILES.get('photos'):
        date = request.POST.get('date')
        description = request.POST.get('description')
        photos = request.FILES['photos']
        WoundHealing.objects.create(patient=request.user, date=date, description=description, photos=photos)

    return render(request, 'heal_wound.html')

@patient_required
def feedback(request):
    name = request.session.get('name')
    if request.method == 'POST':
        name = name
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Feedback.objects.create(name=name, email=email, subject=subject, message=message)
        return redirect('viewfeedback')
    return render(request, 'feedback.html', {'name': name})

@patient_required
def report(request):
    patient = Patient.objects.get(user=request.user)
    reports = Report.objects.filter(patient=patient)
    
    return render(request, 'report.html', {'reports': reports})

@patient_required
def Viewhistory(request):
    user = request.user
    patient = Patient.objects.get(user=user)
    historys = History.objects.filter(patient=patient)
    return render(request, 'history.html', {'historys': historys})

@patient_required
def polls(request):
    polls = Polls.objects.all()
    poll_data = []

    if request.method == "POST":
        poll_id = request.POST.get('poll_id')
        selected_option = request.POST.get('option')
        poll = get_object_or_404(Polls, pk=poll_id)

        # Assuming you are using the User model from django.contrib.auth
        if request.user.is_authenticated:
            if not Answer.objects.filter(user=request.user, poll=poll).exists():
                Answer.objects.create(
                    user=request.user,
                    poll=poll,
                    answer=selected_option)
            else:
                answer = Answer.objects.get(user=request.user, poll=poll)
                answer.answer = selected_option
                answer.save()
        else:
            # Handle case where user is not authenticated
            pass

    for poll in polls:
        poll_info = {
            'poll': poll,
            'option1_count': 0,
            'option2_count': 0,
            'option3_count': 0,
            'option4_count': 0,
            'option1_percentage': 0,
            'option2_percentage': 0,
            'option3_percentage': 0,
            'option4_percentage': 0,
        }
        total_answers = Answer.objects.filter(poll=poll).count()

        if total_answers > 0:
            poll_info['option1_count'] = Answer.objects.filter(poll=poll, answer='option1').count()
            poll_info['option2_count'] = Answer.objects.filter(poll=poll, answer='option2').count()
            poll_info['option3_count'] = Answer.objects.filter(poll=poll, answer='option3').count()
            poll_info['option4_count'] = Answer.objects.filter(poll=poll, answer='option4').count()

            poll_info['option1_percentage'] = (poll_info['option1_count'] / total_answers) * 100
            poll_info['option2_percentage'] = (poll_info['option2_count'] / total_answers) * 100
            poll_info['option3_percentage'] = (poll_info['option3_count'] / total_answers) * 100
            poll_info['option4_percentage'] = (poll_info['option4_count'] / total_answers) * 100

        poll_data.append(poll_info)

    return render(request, 'poll.html', {'poll_data': poll_data})

@patient_required
def addhistory(request):
    if request.method == "POST":
        doctor_id = request.POST.get('doctor')
        plan_id = request.POST.get('plan')
        disease = request.POST.get('disease')
        date = request.POST.get('date')
        
        doctor = Doctor.objects.get(id=doctor_id)
        plan = TreatmentPlan.objects.get(id=plan_id)
        
        History.objects.create(
            patient=request.user.patient,
            doctor=doctor,
            plan=plan,
            disease=disease,
            date=date
        )
        
        return redirect('viewhistory')
    
    doctors = Doctor.objects.all()
    plans = TreatmentPlan.objects.all()
    return render(request, 'addhistory.html', {'doctors': doctors, 'plans': plans})

@patient_required
def viewfeedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'viewfeedback.html', {'feedbacks': feedbacks})