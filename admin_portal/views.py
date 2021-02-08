from datetime import datetime

from django.views.generic.base import TemplateView, View
from .models import CovidQuestionnaire


class HomePageView(TemplateView):
    template_name = "index.html"


class CovidQuestionnairePage(View):
    template_name = "covid_questionnaire.html"


def covid_questionnaire_completed(user_id):
    # queries the database to check if the user has completed the questionnaire today
    latest_questionnaire = CovidQuestionnaire.objects.get(user_id=user_id)
    todays_date = datetime.now().date()
    for i in latest_questionnaire:
        if todays_date == i.time_signed.date():
            return True
    return False
