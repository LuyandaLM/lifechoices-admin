from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import Group

from .forms import RegisterUserForm, GeneralUserUpdateForm, StaffUpdateForm, StudentUpdateForm, LifeChoicesForm, BankingDetailsForm
from .email_confirmation import activate_email
from admin_portal.models import User, LifeChoicesMember, LifeChoicesAcademy, LifeChoicesStuff


class Register(View):
    """
    registration form for new users
    """
    form_class = RegisterUserForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        """
        what will be returned when the user requests this page using the link user/register
        :param request: the request
        :param args:
        :param kwargs:
        :return: the page with the form the user has to complete
        """
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)   # completed form
        if form.is_valid():
            form.save()
            email = form.cleaned_data["email"]
            username = form.cleaned_data.get('username')
            user = User.objects.filter(email=email).first()
            role = form.cleaned_data["roles"]
            # add groups to user
            if role == "visitor":
                group = Group.objects.get(name='visitor')
                user.groups.add(group)
            elif role == 'business_unit':
                group = Group.objects.get(name='business_unit')
                user.groups.add(group)
            elif role == '	staff':
                group = Group.objects.get(name='staff')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='student')
                user.groups.add(group)

            messages.success(
                request, f'{username} your account has been created! You are now able to log in')
            return redirect('users:login')
        else:
            return render(request, self.template_name, {'form': form})


@login_required
def profile(request):
    user = request.user
    # load form specific to user
    user_form = GeneralUserUpdateForm(instance=user)

    if request.method == "GET":
        if additional_forms(request)[1]:
            context = {
                # 'form': user_form,
                # 'life_choices_form': additional_forms(request)[0],
                'formset': additional_forms(request)[1],
            }
        else:
            context = {
                'form': user_form,
            }
        return render(request, 'profile.html', context=context)

    if request.method == 'POST':
        user_form = GeneralUserUpdateForm(request.POST, request.FILES, instance=user)
        # saving the general form
        if user_form.is_valid():
            user_form.save()
            # only users that are life choices can submit this forms
            if additional_forms(request)[0]:
                print('im here')
                # basic details required from a life choices member
                member = LifeChoicesMember.objects.filter(user=request.user).first()
                life_choices_form = LifeChoicesForm(request.POST, instance=member)
                if life_choices_form.is_valid():
                    life_choices_form.save()
                if request.user.roles == 'business_unit' or 'staff':
                    print('im a b or sta')
                    instance = LifeChoicesStuff.objects.filter(user=member).first()
                    formset = StaffUpdateForm(request.POST, instance=instance)
                    if formset.is_valid():
                        formset.save()
                elif request.user.roles == 'student':
                    print('im a stu')
                    formset = StudentUpdateForm(request.POST, instance=request.user)
                    if formset.is_valid():
                        formset.save()
        messages.success(request, f'account update successfully')
        return redirect('users:profile')


def additional_forms(request):
    formset = None
    member = LifeChoicesMember.objects.filter(user=request.user).first()
    life_choices_form = LifeChoicesForm(instance=member)
    if request.user.roles == 'business_unit' or 'staff':
        instance = LifeChoicesStuff.objects.filter(user=member).first()
        formset = StaffUpdateForm(instance=instance)
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
    messages.success(
        request, f"{user.user_name}'s account activated successfully")
    activate_email(user)
    return redirect('users:pending-accounts')


class ViewProfile(View):
    template_name = 'account_profile.html'

    def get(self, request):
        context = {}
        form = BankingDetailsForm()
        context['form'] = form
        return render(self.request, self.template_name, context)

    def post(self, request):
        form = BankingDetailsForm(self.request.POST)
        if form.is_valid():
            form.save()
        return redirect('store:viewprofile')


class AdminPageView(View):
    template_name = "admin.html"

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)
