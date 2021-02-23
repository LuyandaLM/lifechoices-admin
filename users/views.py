from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import Group

from .forms import RegisterUserForm, BankingDetailsForm, BasicInfoForm, NextOfKinForm, ContactDetailsForm
from admin_portal.models import User, LifeChoicesMember, LifeChoicesAcademy, BankingDetail


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
            email = form.cleaned_data["email"]
            username = form.cleaned_data.get('username')
            user = User.objects.filter(email=email).first()
            role = form.cleaned_data["roles"]
            user = form.save(commit=False)
            user.save()
            # add groups to
            user_group = ''
            if role == "visitor":
                user_group = Group.objects.get(name='visitor')
            elif role == 'business_unit':
                user_group = Group.objects.get(name='business_unit')
            elif role == '	staff':
                user_group = Group.objects.get(name='staff')
            else:
                user_group = Group.objects.get(name='student')

            user.groups.add(user_group)
            messages.success(
                request, f'{username} your account has been created! You are now able to log in')
            return redirect('users:login')
        else:
            return render(request, self.template_name, {'form': form})


""" def profile(request):
    user = request.user
    # load form specific to user
    user_form = GeneralUserUpdateForm(instance=user)
    if user.groups.filter(name='visitor').exists():
        user_form = GeneralUserUpdateForm(instance=user)
    elif user.groups.filter(name='business_unit').exists():
        user_form = StaffUpdateForm(instance=user)
    elif user.groups.filter(name='staff').exists():
        user_form = StaffUpdateForm(instance=user) 
    elif user.groups.filter(name='student').exists():
        user_form = StudentUpdateForm(instance=user)

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
        if user.groups.filter(name='visitor').exists():
            user_form = GeneralUserUpdateForm(
                request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                user_form.save()
        elif user.groups.filter(name='business_unit').exists():
            user_form = StaffUpdateForm(
                request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                print(request.POST)
                user_form.save()
        elif user.groups.filter(name='staff').exists():
            user_form = StaffUpdateForm(
                request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                user_form.save()
        elif user.groups.filter(name='student').exists():
            user_form = StudentUpdateForm(
                request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                user_form.save()

        messages.success(request, f'account update successfully')
        return redirect('users:profile') """


""" def additional_forms(request):
    formset = None
    member = LifeChoicesMember.objects.filter(user=request.user).first()
    life_choices_form = LifeChoicesForm(instance=member)
    if request.user.roles == 'business_unit' or 'staff':
        instance = Bankingdetails.objects.filter(user=member).first()
        formset = StaffUpdateForm(instance=instance)
    elif request.user.roles == 'student':
        formset = StudentUpdateForm(instance=request.user)
    return life_choices_form, formset """


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
    messages.success(
        request, f"{user.user_name}'s account activated successfully")
    return redirect('users:pending-accounts')


class ViewProfile(View):
    template_name = 'profile/profile.html'

    def get(self, *args, **kwargs):
        context = {}
        form = BankingDetailsForm()
        context['form'] = form
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = BankingDetailsForm(self.request.POST)
        if form.is_valid():
            form.save()
        return redirect('store:viewprofile')


def update_profile(request, pk):
    context = {}
    user = User.objects.get(id=pk)
    form = BasicInfoForm(instance=user)
    context['form'] = form
    if request.method == 'POST':
        form = BasicInfoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:viewprofile')
    return render(request, 'profile/updateprofile.html', context)


def update_bankingdetails(request):
    context = {}
    user = request.user.id
    details = BankingDetail.objects.filter(user=user).first()
    form = BankingDetailsForm(instance=details)
    context['form'] = form
    if request.method == 'POST':
        form = BankingDetailsForm(instance=details, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:viewprofile')
    return render(request, 'profile/updatebankingdetails.html', context)


def update_contact_details(request):
    context = {}
    user = request.user.id
    details = User.objects.filter(id=user).first()
    form = ContactDetailsForm(instance=details)
    context['form'] = form
    if request.method == 'POST':
        form = ContactDetailsForm(instance=details, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:viewprofile')
    return render(request, 'profile/updatecontactdetails.html', context)


def update_kin_details(request):
    context = {}
    user = request.user.id
    details = User.objects.filter(id=user).first()
    form = NextOfKinForm()
    context['form'] = form
    if request.method == 'POST':
        form = NextOfKinForm(instance=details, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:viewprofile')
    return render(request, 'profile/updatenextofkin.html', context)
