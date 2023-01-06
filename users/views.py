from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView


# Create your views here.
class LoginView(CreateView):
    form_class = LoginForm
    template_name = 'users/login.html'
    success_url = '/products/'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form_class
        }

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user:
                login(request, user=user)
                return redirect('/products/')
            else:
                form.add_error('username', 'bad request!')

        return render(request, self.template_name, context={
            'form': form,
            'user': None if request.user.is_anonymous else request.user
        })


class Logout(ListView):
    def get(self, request, **kwargs):
        logout(request)
        return redirect('/products/')


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': self.form_class
        }

    def post(self, request, *args, **kwargs):
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            if form.cleaned_data.get("password_1") == form.cleaned_data.get("password_2"):
                user = User.objects.create_user(
                    username=form.cleaned_data.get("username"),
                    password=form.cleaned_data.get("password_2")
                )
                login(request, user)
                return redirect('/products/')
            else:
                form.add_error("password_2", 'bad request!')

        return render(request, self.template_name, context={
            'form': form
        })


# def register_view(request):
#     if request.method == "GET":
#         context = {
#             'form': RegisterForm
#         }
#
#         return render(request, 'users/register.html', context=context)
#
#     if request.method == "POST":
#         form = RegisterForm(data=request.POST)
#
#         if form.is_valid():
#             if form.cleaned_data.get("password_1") == form.cleaned_data.get("password_2"):
#                 user = User.objects.create_user(
#                     username=form.cleaned_data.get("username"),
#                     password=form.cleaned_data.get("password_2")
#                 )
#                 login(request, user)
#                 return redirect('/products/')
#             else:
#                 form.add_error("password_2", 'bad request!')
#
#         return render(request, 'users/register.html', context={
#             'form': form
#         })
