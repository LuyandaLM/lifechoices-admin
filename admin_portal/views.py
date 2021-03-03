from datetime import datetime

from django.shortcuts import render
from django.views.generic import View, ListView
from django.shortcuts import redirect
from django.contrib import messages

from .models import CovidQuestionnaire, User, LeaveApplication, LifeChoicesMember, BankingDetail
from .models import CovidQuestionnaire, User, LeaveApplication, LifeChoicesMember, LifeChoicesAcademy, BankingDetail
from .forms import CovidForm
#from .writing_to_csv import write_to_check_in_csv
from .location.location import get_current_location


class HomePageView(View):
    template_name = "index.html"
    # write_to_check_in_csv()

    def get(self, request, *args, **kwargs):
        if not covid_questionnaire_completed(request.user.id):
            messages.success(
                request, f'{request.user.user_name} Please complete covid questionnaire before proceeding')
            return redirect('admin_portal:covid-questionnaire')
        if request.user.roles == 'visitor':
            return redirect('https://www.lifechoices.co.za/')
        context = {
            'pending_accounts': User.objects.filter(is_active=False),
            'leaves_applications': LeaveApplication.objects.all()
        }
        return render(request, self.template_name, context=context)


class CovidQuestionnairePage(View):
    form_class = CovidForm
    initial = {'key': 'value'}
    template_name = "covid_questionnaire.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CovidForm(request.POST)
        if form.is_valid():
            user = request.user
            covid_questionnaire = CovidQuestionnaire(user=user, temperature=form.cleaned_data['temperature'],
                                                     Shortness_of_breath=form.cleaned_data['Shortness_of_breath'],
                                                     sore_throat=form.cleaned_data['sore_throat'],
                                                     loss_of_taste_or_smell=form.cleaned_data[
                                                         'loss_of_taste_or_smell'],
                                                     contact_with_Covid=form.cleaned_data['contact_with_Covid'],
                                                     nasal_congestion=form.cleaned_data['nasal_congestion'],
                                                     diarrhea=form.cleaned_data['diarrhea'],
                                                     nausea=form.cleaned_data['nausea'])
            covid_questionnaire.save()
            messages.success(
                request, f'{user.user_name} form completed successfully')
            return redirect('admin_portal:home')
        else:
            form = CovidForm()
            return render(request, self.template_name, {'form': form})


def covid_questionnaire_completed(user_id):
    # queries the database to check if the user has completed the questionnaire today
    latest_questionnaire = CovidQuestionnaire.objects.filter(user_id=user_id)
    todays_date = datetime.now().date()
    for i in latest_questionnaire:
        if todays_date == i.time_in.date():
            return True
    return False


class LeaveApplicationPage(View):
    initial = {'key': 'value'}
    template_name = "request_leave.html"

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        member = LifeChoicesMember.objects.filter(user=request.user).first()
        leave_type = request.POST.getlist("leave")[0]
        start_date = request.POST.getlist("start_date")[0]
        end_date = request.POST.getlist("end_date")[0]
        message = request.POST.getlist("message")[0]
        file = request.POST.getlist("file")
        leave = LeaveApplication(user=member, category=leave_type, personal_message=message, leave_date_from=start_date,
                                 leave_date_to=end_date)
        leave.save()
        return render(request, self.template_name)


class PendingLeaveApplicationPage(ListView):
    template_name = "pending_leave.html"
    model = LeaveApplication
    queryset = LeaveApplication.objects.all()
    context_object_name = "leave_applications"


class ChatPageView(View):
    template_name = "chat.html"

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)


class BankingDetailPageView(View):
    template_name = "check_in.html"

    def get(self, request, *args, **kwargs):
        if already_checked_in(request.user):
            messages.success(
                request, f'{request.user.user_name} you have already checked-in')
            return redirect('admin_portal:home')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = request.user
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        current_location = get_current_location(latitude, longitude)
        location = current_location['display_name']
        # user_check_in = BankingDetail(user=user, location=(
        # current_location['display_name']))
        # user_check_in.save()
        messages.success(
            request, f"{user.user_name} you have checked-in at {location}")
        return redirect('admin_portal:home')


class BankingDetailOffsitePageView(View):
    template_name = "BankingDetailoffsite.html"

    def get(self, request, *args, **kwargs):
        if already_checked_in(request.user):
            messages.success(
                request, f'{request.user.user_name} you have already checked-in')
            return redirect('admin_portal:home')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = request.user
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        remote_work = False
        if request.POST['remote_work'] == 'on':
            remote_work = True
        current_location = get_current_location(latitude, longitude)
        location = current_location['display_name']
        user_check_in = BankingDetail(user=user, location=(
            current_location['display_name']), remote_work=remote_work)
        user_check_in.save()
        messages.success(
            request, f"{user.user_name} you have checked-in at {location}")
        return redirect('admin_portal:home')


def already_checked_in(user):
    check_in_locations = BankingDetail.objects.filter(user=user)
    todays_date = datetime.now().date()
    for check_in in check_in_locations:
        if todays_date == check_in.time_signed_in.date():
            print('im here')
            return True
    return False


class AccountProfilePageView(View):
    template_name = "accountprofile.html"

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)


class PrintUsersPageView(View):
    template_name = "printusers.html"

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)


class PrintCovidPageView(View):
    template_name = "printcovid.html"

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)


class CovidForPageView(View):
    template_name = "covidfor.html"

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)


class CalendarPageView(View):
    template_name = "cal.html"

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)


def error_404(request, exception):
    data = {}
    return render(request, 'error_handling_pages/404.html', data)


def error_500(request, *args, **kwargs):
    data = {}
    return render(request, 'error_handling_pages/500.html', data)


def error_403(request, exception):
    data = {}
    return render(request, 'error_handling_pages/403.html', data)


def error_400(request, exception):
    data = {}
    return render(request, 'error_handling_pages/400.html', data)


def error_204(request, exception):
    data = {}
    return render(request, 'error_handling_pages/204.html', data)


def error_401(request, exception):
    data = {}
    return render(request, 'error_handling_pages/401.html', data)


def error_402(request, exception):
    data = {}
    return render(request, 'error_handling_pages/402.html', data)


class CheckOutlcPageView(View):
    template_name = "checkoutlc.html"

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)


class CheckOutoffPageView(View):
    template_name = "checkoutoff.html"

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name)
