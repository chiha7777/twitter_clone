from django.views.generic import TemplateView, CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


from .forms import SignUpForm

User = get_user_model()

class IndexView(TemplateView):
    template_name = "accounts/index.html"

class HomeView(TemplateView):
    template_name = "accounts/home.html"

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)
