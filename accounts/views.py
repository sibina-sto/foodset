from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, CreateView, UpdateView
from django.contrib.auth import logout
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.contrib.messages.views import SuccessMessageMixin



class LogoutView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        logout(request)
        return redirect('home')


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_message = "Account Created Successfully"
    success_url = reverse_lazy('login')


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = RegisterForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('my_posts')
    success_message = "Profile Updated Successfully"

    def get_object(self, queryset=None):
        return self.request.user


class ImageUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile_picture.html'

    @staticmethod
    def post(request, *args, **kwargs):
        # Get the uploaded image from the form data
        img = request.FILES.get('image')

        if img and img.content_type.startswith('image'):
            # Use get_or_create to simplify the code
            profile, created = Profile.objects.get_or_create(user=request.user)

            # Update the profile's image and save it
            profile.image = img
            profile.save()

            # Redirect to the user's profile page
            return redirect('profile', request.user.id)
        else:
            # Handle invalid or missing image file
            return render(request, 'error_page.html', {'error_message': 'Invalid or missing image file'})