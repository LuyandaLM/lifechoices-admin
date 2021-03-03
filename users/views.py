from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import Group

from .forms import RegisterUserForm, BankingDetailsForm, BasicInfoForm, NextOfKinForm, ContactDetailsForm, RegisterformTwo
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
            role = form.cleaned_data["roles"]
            user = User.objects.filter(email=email).first()
            user = form.save(commit=False)
            user.save()
            # add groups to
            user_group = ''
            if role == "visitor":
                user_group = Group.objects.get(name='visitor')
                user.groups.add(user_group)
                return redirect('users:login')

            elif role == 'business_unit':
                user_group = Group.objects.get(name='business_unit')
            elif role == '	staff':
                user_group = Group.objects.get(name='staff')
            else:
                user_group = Group.objects.get(name='student')

            user.groups.add(user_group)
            messages.success(
                request, f'{email} your account has been created! You are now able to log in')
            return redirect('users:registerp2')
        else:
            return render(request, self.template_name, {'form': form})


class RegisterParttwo(View):
    form_class = RegisterformTwo
    template_name = 'register2.html'
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = self.form_class(initial=self.initial)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return redirect('https://www.lifechoices.co.za/')


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
