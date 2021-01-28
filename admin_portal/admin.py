from django.contrib import admin
from .models import User, CovidQuestionnaire, LeaveApplication, LifeChoicesMember, LifeChoicesAcademy, LifeChoicesStuff

admin.site.register(User)
admin.site.register(CovidQuestionnaire)
admin.site.register(LeaveApplication)
admin.site.register(LifeChoicesMember)
admin.site.register(LifeChoicesAcademy)
admin.site.register(LifeChoicesStuff)
