from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Patient

def patient_required(view_func):
    @login_required(login_url='/login/')  
    def _wrapped_view(request, *args, **kwargs):
        try:
            request.user.patient
        except Patient.DoesNotExist:
            auth_logout(request)
            return HttpResponseRedirect(reverse('login'))  
        return view_func(request, *args, **kwargs)
    return _wrapped_view
