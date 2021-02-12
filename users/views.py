from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import Group

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
            if form.cleaned_data["roles"] == "visitor":
                group = Group.objects.get(name='visitor')
                user = User.objects.filter(email=form.cleaned_data["email"]).first()
                user.groups.add(group)

            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} your account has been created! You are now able to log in')
            return redirect('users:login')
        else:
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
        if user_form.is_valid():
            user_form.save()
            if request.user.roles != "visitor":
                life_choices_form = LifeChoicesForm(request.POST, instance=request.user)
                if request.user.roles == "student":
                    formset = StudentUpdateForm(instance=request.user)
                elif request.user.roles == "staff" or "business_unit":
                    formset = StaffUpdateForm(instance=request.user)
                if life_choices_form.is_valid() and formset.is_valid():
                    life_choices_form.save()
                    formset.save()
            messages.success(request, f'account update successfully')
        else:
            print("this is user_form errors ")
        return redirect('users:profile')


def additional_forms(request):
    life_choices_form = LifeChoicesForm(instance=request.user)
    if request.user.roles == 'business_unit' or 'staff':
        formset = StaffUpdateForm(instance=request.user)
    elif request.user.roles == 'student':
        formset = StudentUpdateForm(instance=request.user)
    return life_choices_form, formset


class PendingAccounts(ListView):
    template_name = "pending_accounts.html"
    model = User
    queryset = User.objects.filter(is_active=False)
    context_object_name = "accounts"


class ActivatePendingAccount(DetailView):
    template_name = "account.html"
    queryset = User.objects.all()
    context_object_name = "user"


def activate_account(request, pk):
    user = User.objects.filter(pk=pk).first()
    user.is_active = True
    user.save()
    member = LifeChoicesMember.objects.create(user=user)
    if user.roles == 'business_unit' or 'staff':
        if user.roles == 'business_unit':
            group = Group.objects.get(name='business_unit')
        elif user.roles == 'staff':
            group = Group.objects.get(name='staff')
        LifeChoicesStuff.objects.create(user=member)
    elif user.roles == 'student':
        group = Group.objects.get(name='student')
        LifeChoicesAcademy.objects.get_or_create(user=member)
    user.groups.add(group)
    user.save()
    messages.success(request, f"{user.user_name}'s account activated successfully")
    return redirect('users:pending-accounts')