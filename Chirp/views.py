from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.forms import forms

from django.views.generic import FormView

from django.contrib.auth.views import LoginView
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

class LoginView(LoginView):
    template_name = "Chirp/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")
    
class SignupView(FormView):
    template_name = "Chirp/signup.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignupView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super(SignupView, self).get(*args, **kwargs)



@login_required(login_url='login')
def home(request):
    return render(request, 'Chirp/home.html')