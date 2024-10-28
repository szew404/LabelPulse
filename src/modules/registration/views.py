from .forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import Group
from django.shortcuts import render


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("signup_success")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        # User notification

        # User config
        user = self.object
        user.is_staff = True
        label_manager_group, created = Group.objects.get_or_create(name="Label Manager")
        user.groups.add(label_manager_group)
        user.save()

        return response


def success_signup(request):
    return render(request, "registration/success_signup.html")
