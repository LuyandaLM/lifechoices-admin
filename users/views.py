from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

from .forms import RegisterUserForm, GeneralUserUpdateForm, StaffUpdateForm, StudentUpdateForm, LifeChoicesForm
from admin_portal.models import User, LifeChoicesMember, LifeChoicesAcademy, LifeChoicesStuff


class Register(View):
    form_class = RegisterUserForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} your account has been created! You are now able to log in')
            return redirect('users:login')
        else:
            form = RegisterUserForm()
            return render(request, self.template_name, {'form': form})


@login_required
def profile(request):
    user_form = GeneralUserUpdateForm(instance=request.user)
    if request.method == "GET":
        if additional_forms(request)[1]:
            context = {
                'form': user_form,
                'life_choices_form': additional_forms(request)[0],
                'formset': additional_forms(request)[1],
            }
        else:
            context = {
                'form': user_form,
            }
        return render(request, 'profile.html', context=context)

    if request.method == 'POST':
        user_form = GeneralUserUpdateForm(request.POST, request.FILES, instance=request.user)
        # print(user_form)
        if user_form.is_valid():
            user_form.save()
            if request.user.roles != "visitor":
                life_choices_form = LifeChoicesForm(request.POST, instance=request.user)
                if request.user.roles == "student":
                    formset = StaffUpdateForm(instance=request.user)
                elif request.user.roles == "staff" or "business_unit":
                    formset = StudentUpdateForm(instance=request.user)
                if life_choices_form.is_valid():
                    print("im valid")
                if formset.is_valid():
                    print("im valid")
            if additional_forms(request):
                print("love")
        # if user_form.is_valid() and formset.is_valid() and life_choices_form.is_valid():
        #     print("all forms are valid")
        else:
            print("this is user_form errors ")
        return redirect('users:profile')
    # else:
    #     form = SimpleUserForm(instance=request.user)
    #


def additional_forms(request):
    life_choices_form = LifeChoicesForm(instance=request.user)
    if request.user.roles == 'business_unit' or 'staff':
        print()
        formset = StaffUpdateForm(instance=request.user)
    elif request.user.roles == 'student':
        formset = StudentUpdateForm(instance=request.user)
    return life_choices_form, formset
