from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

from .forms import RegisterUserForm


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
    # if request.method == 'POST':
    #     u_form = SimpleUserForm(request.POST, instance=request.user)
    #     p_form = AdminForm(request.POST, instance=request.user)
    #     if request.user in Intern.objects.all():
    #         p_form = InternUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    #     elif request.user in Partner.objects.all():
    #         p_form = PartnerForm(request.POST, request.FILES, instance=request.user.profile)
    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         messages.success(request, f'Your Account Has Been Updated!')
    #         return redirect('profile')
    # else:
    #     form = SimpleUserForm(instance=request.user)
    #
    # context = {
    #     'u_form': u_form,
    #     'p_form': p_form
    # }
    return render(request, 'profile.html')  # context)
