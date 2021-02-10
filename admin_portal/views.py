from datetime import datetime

from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages

from .models import CovidQuestionnaire
from .forms import CovidForm


class HomePageView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        if not covid_questionnaire_completed(request.user.id):
            messages.success(request, f'{request.user.user_name} Please complete covid questionnaire before proceeding')
            return redirect('admin_portal:covid-questionnaire')
        if request.user.roles == 'visitor':
            return redirect('https://www.lifechoices.co.za/')
        return render(request, self.template_name)


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
                                                     loss_of_taste_or_smell=form.cleaned_data['loss_of_taste_or_smell'],
                                                     contact_with_Covid=form.cleaned_data['contact_with_Covid'],
                                                     nasal_congestion=form.cleaned_data['nasal_congestion'],
                                                     diarrhea=form.cleaned_data['diarrhea'],
                                                     nausea=form.cleaned_data['nausea'])
            print(covid_questionnaire.user)
            covid_questionnaire.save()
            messages.success(request, CovidQuestionnaire.objects.all())
            messages.success(request, f'{user.user_name} form completed successfully')
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
