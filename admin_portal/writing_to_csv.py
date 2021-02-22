from .models import *
import csv


def write_to_covid_csv():
    questionnaires = CovidQuestionnaire.objects.all()
    with open('questionnaire.csv', mode='w') as questionnaire_file:
        fieldnames = ["temperature", "Shortness_of_breath", "sore_throat", "loss_of_taste_or_smell",
                      "contact_with_Covid", "nasal_congestion", "diarrhea", "nausea", "User"]
        writer = csv.DictWriter(questionnaire_file, fieldnames=fieldnames)
        writer.writeheader()
        for questionnaire in questionnaires:
            writer.writerow({'temperature': questionnaire.temperature,
                             "Shortness_of_breath": questionnaire.Shortness_of_breath,
                             "sore_throat":questionnaire.sore_throat,
                             "loss_of_taste_or_smell": questionnaire.loss_of_taste_or_smell,
                             "contact_with_Covid": questionnaire.contact_with_Covid,
                             "nasal_congestion": questionnaire.nasal_congestion,
                             "diarrhea": questionnaire.diarrhea,
                             "nausea": questionnaire.nausea,
                             "User": questionnaire.user})

        return questionnaire_file


def write_to_user_csv():
    users = User.objects.all()
    with open('users.csv', mode='w') as users_file:
        fieldnames = ['email', 'user_name', 'first_name', 'last_name', 'gender', 'roles', 'marital_status',
                      'date_of_birth', 'nationality', 'address', 'telephone_number', 'cell_number', 'permanent_address',
                      'next_of_kin_name', 'permanent_telephone_number', 'next_of_kin_relationship',
                      'next_of_kin_contact_number']
        writer = csv.DictWriter(users_file, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow({'email': user.email, 'user_name': user.user_name, 'first_name': user.first_name,
                             'last_name': user.last_name, 'gender': user.gender, 'roles': user.roles,
                             'marital_status': user.marital_status, 'date_of_birth': user.date_of_birth,
                             'nationality': user.nationality, 'address': user.address,
                             'telephone_number': user.telephone_number, 'cell_number': user.cell_number,
                             'permanent_address':user.permanent_address, 'next_of_kin_name': user.next_of_kin_name,
                             'permanent_telephone_number': user.permanent_telephone_number,
                             'next_of_kin_relationship': user.next_of_kin_relationship,
                             'next_of_kin_contact_number': user.next_of_kin_contact_number})

        return users_file


def write_to_leave_csv():
    leaves = LeaveApplication.objects.all()
    with open('leave.csv', mode='w') as leave_file:
        fieldnames = ["category", "personal_message", "leave_date_from", "leave_date_to", "pre_authorisation"]
        writer = csv.DictWriter(leave_file, fieldnames=fieldnames)
        writer.writeheader()
        for leave in leaves:
            writer.writerow({"category": leave.category,
                             "personal_message": leave.personal_message,
                             "leave_date_from": leave.leave_date_from,
                             "leave_date_to": leave.leave_date_to,
                             "pre_authorisation": leave.pre_authorisation,})

        return leave_file
