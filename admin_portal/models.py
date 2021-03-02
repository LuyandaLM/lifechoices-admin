from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from PIL import Image


# Custom Account manager
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):

        # Default fields
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        other_fields.setdefault('first_name', 'First Name')
        other_fields.setdefault('last_name', 'Last Name')

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        if other_fields.get('is_active') is not True:
            raise ValueError('Superuser must be assigned to is_active=True')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        other_fields.setdefault('user_name', 'Username')
        other_fields.setdefault('first_name', 'First Name')
        other_fields.setdefault('last_name', 'Last Name')
        user = self.model(email=email, password=password, **other_fields)
        user.set_password(password)
        user.save()
        return user


# custom user with email as username
# changing newuser to user
class User(AbstractBaseUser, PermissionsMixin):
    role = (
        ("staff", "STAFF"),
        ("business_unit", "BUSINESS UNIT"),
        ("student", "STUDENT"),
        ("visitor", "VISITOR"),
    )
    gender_choices = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    marital_choices = (
        ("single", "Single"),
        ("married", "Married"),
        ("widowed", "Widowed"),
        ("divorced", "Divorced"),
    )

    # signup fields
    image = models.ImageField(
        null=True, blank=True, default="profile_pictures/default.jpg", upload_to='profile_pictures/')
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    # Employee identification
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # Personal details
    gender = models.CharField(choices=gender_choices, max_length=6)
    date_of_birth = models.DateField(
        "Date of birth(mm/dd/yyyy) ", auto_now_add=False, auto_now=False, blank=True, null=True)
    marital_status = models.CharField(choices=marital_choices, max_length=20)
    nationality = models.CharField(max_length=50)
    identity_number = models.CharField(max_length=20, null=True, blank=True)

    # Contact info
    address = models.TextField(max_length=200)
    telephone_number = models.CharField(max_length=15, null=False, blank=False)
    cell_number = models.CharField(max_length=15, null=False, blank=False)

    # Permanent address
    permanent_address = models.TextField(max_length=200, null=True, blank=True)
    permanent_telephone_number = models.CharField(
        max_length=15, null=False, blank=False)

    # authentication
    roles = models.CharField(max_length=15, choices=role, default="visitor")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    # group = models.CharField(max_length=150, null=False, blank=False)

    # Next of Kin
    next_of_kin_name = models.CharField(max_length=50)
    next_of_kin_relationship = models.CharField(max_length=50)
    next_of_kin_contact_number = models.CharField(max_length=15)

    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="last login", auto_now=True, null=True)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f' {self.email}'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    # image re-sizing using PIL
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class LifeChoicesMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ID_number = models.BigIntegerField(null=True, blank=False)
    chronic_condition = models.CharField(max_length=50, null=True, blank=False)
    allergies = models.CharField(max_length=50, null=True, blank=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


# life-choice members
class LifeChoicesAcademy(models.Model):
    user = models.ForeignKey(LifeChoicesMember, on_delete=models.CASCADE)
    student_number = models.CharField(max_length=13, null=True, blank=False)

    def __str__(self):
        return self.user.user.user_name


# life choices stuff
class BankingDetail(models.Model):
    user = models.ForeignKey(LifeChoicesMember, on_delete=models.CASCADE)
    # Banking details
    bank_name = models.CharField(max_length=50, null=True, blank=False)
    account_holder_name = models.CharField(
        max_length=50, null=True, blank=False)
    account_number = models.CharField(max_length=50, null=True, blank=False)
    branch_name = models.CharField(max_length=50, null=True, blank=False)
    branch_number = models.CharField(max_length=50, null=True, blank=False)
    # chronic illness and allergies
    tax_number = models.CharField(max_length=25, null=True, blank=False)

    def __str__(self):
        return f'{self.user.user.first_name} {self.user.user.last_name}'


# Covid Questionnaires
class CovidQuestionnaire(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # info
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    Shortness_of_breath = models.BooleanField(default=True)
    sore_throat = models.BooleanField(default=True)
    loss_of_taste_or_smell = models.BooleanField(default=True)
    contact_with_Covid = models.BooleanField(default=True)
    nasal_congestion = models.BooleanField(default=True)
    diarrhea = models.BooleanField(default=True)
    nausea = models.BooleanField(default=True)
    time_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Covid questionnaire taken by {self.user} on {self.time_in}"


# Leave Application
class LeaveApplication(models.Model):
    """
    leave application can only be done by lifechoices stuff and not general and lifechoices members
    """
    CATEGORY = (
        ('Annual Leave', 'Annual Leave'),
        ('Sick Leave', 'Sick Leave'),
        ('Family Leave', 'Family Leave'),
        ('Unpaid Leave', 'Unpaid Leave'),
        ('Study Leave', 'Study Leave'),
        ('Compensation Leave', 'Compensation Leave'),
        ('Other Leave', 'Other Leave')
    )
    user = models.ForeignKey(LifeChoicesMember, on_delete=models.CASCADE)

    # info
    category = models.CharField(
        max_length=45, null=False, blank=False, choices=CATEGORY)
    pre_authorisation = models.BooleanField(
        default=False, blank=False, null=False)
    personal_message = models.CharField(max_length=200, null=True, blank=True)
    leave_date_from = models.DateField(blank=False, null=False)
    leave_date_to = models.DateField(blank=False, null=False)

    # def __str__(self):
    #     return f"Leave request by {self.user} from {self.leave_date_from} - {self.leave_date_to}"


class CheckIn(models.Model):
    """
    the checkin time of the user along with the location they are signing into
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)
    time_signed_in = models.DateTimeField(auto_now_add=True)
    remote_work = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} signed in at {self.location} at the time of {self.time_signed_in}"
