from django import forms
from admin_portal.models import CovidQuestionnaire
from django.forms import Textarea, NullBooleanSelect, NullBooleanField, NumberInput


class CovidForm(forms.ModelForm):
    class Meta:
        model = CovidQuestionnaire
        fields = ["temperature", "Shortness_of_breath", "sore_throat", "loss_of_taste_or_smell", "contact_with_Covid",
                  "nasal_congestion", "diarrhea", "nausea"]
        widgets = {
            "temperature": NumberInput,
            "Shortness_of_breath": NullBooleanSelect(),
            "sore_throat": NullBooleanSelect(),
            "loss_of_taste_or_smell": NullBooleanSelect(),
            "contact_with_Covid": NullBooleanSelect(),
            "nasal_congestion": NullBooleanSelect,
            "diarrhea": NullBooleanSelect(),
            "nausea": NullBooleanSelect()
        }
