from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
# Create your models here.

class Applicant(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, default='NMN')
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Nonbinary')])
    date_of_birth = models.DateField()
    current_school = models.CharField(max_length=200)
    current_grade = models.CharField(max_length=200)
    has_sibling = models.BooleanField(null=True)
    sibling_name = models.CharField(max_length=200, null=True, blank=True)
    sibling_grade = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    lottery_status = models.CharField(max_length=200, null=True, blank=True,
                            choices=[
                                        ('Lottery', 'Lottery'),
                                        ('Waitlist', 'Waitlist'),
                                        ('Admitted', 'Admitted'),
                                        ('Registered', 'Registered'),
                                        ('Declined', 'Declined')
                                    ],
                            default='Lottery')
    waitlist_number = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class SchoolYear(models.Model):
    school_year = models.CharField(max_length=200)
    form_display_value = models.CharField(max_length=200)
    display_on_form = models.BooleanField()

    def __str__(self):
        return f'{self.school_year}'

class Application(models.Model):
    school = models.CharField(max_length=200)
    school_year = models.CharField(max_length=200)
    application_date = models.DateTimeField(default=timezone.now)
    grade = models.CharField(max_length=200)
    how_did_you_hear = models.CharField(max_length=200, null=True)
    other_hear_option =  models.CharField(max_length=200, null=True)
    agree_to_terms = models.BooleanField(null=True)
    applicant = models.ForeignKey(Applicant, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return f'Application for {self.applicant.first_name} {self.applicant.last_name}'


class Address(models.Model):
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=5, null=True)
    applicant = models.ForeignKey(Applicant, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.applicant.first_name} {self.applicant.last_name}'

class PrimaryParent(models.Model):
    name =  models.CharField(max_length=200)
    relation =  models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    applicant = models.ForeignKey(Applicant, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.applicant.first_name} {self.applicant.last_name}'

class SecondaryParent(models.Model):
    secondary_parent_name =  models.CharField(max_length=200, null=True)
    secondary_parent_relation =  models.CharField(max_length=200, null=True)
    secondary_parent_email = models.EmailField(null=True)
    secondary_parent_phone_number = models.CharField(max_length=12, null=True)
    applicant = models.ForeignKey(Applicant, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.applicant.first_name} {self.applicant.last_name}'
