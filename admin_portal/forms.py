from django import forms
from admin_portal.models import CovidQuestionnaire


class CovidForm(forms.ModelForm):
    class Meta:
        model = CovidQuestionnaire
        fields = ["temperature", "Shortness_of_breath", "sore_throat", "loss_of_taste_or_smell", "contact_with_Covid",
                  "nasal_congestion", "diarrhea", "nausea"]