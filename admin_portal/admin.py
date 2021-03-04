from django.contrib import admin
from .models import User, CovidQuestionnaire, LeaveApplication, LifeChoicesMember, LifeChoicesAcademy, BankingDetail, \
    BankingDetail

admin.site.register(User)
admin.site.register(CovidQuestionnaire)
admin.site.register(LeaveApplication)
admin.site.register(LifeChoicesMember)
admin.site.register(LifeChoicesAcademy)
admin.site.register(BankingDetail)
# admin.site.register(BankingDetail)

admin.site.site_header = "Administration"
