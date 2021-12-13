from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView


# Create your views here.
class CustomLoginView(LoginView):
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "Úspešne ste boli prihlásený."
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exclude_header"] = True

        return context


def logout_view(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.SUCCESS, "Úspešne ste boli odhlásený.")

    logout(request)
    return redirect("login")
