from django.core.mail import send_mail
from . models import Applicant
from django.db.models import F, Count

def get_application_data(school, school_year):
    data = Applicant.objects.values(
                            school=F('application__school'),
                            grade=F('application__grade'),
                            city=F('address__city'),
                            year=F('application__school_year')
                           ).filter(
                            school__in=[school, 'Both Schools'],
                            year=school_year
                           )
    return data

def get_application_counts(school, year):
    cities = Applicant.objects.filter(
                            application__school__in=[school, 'Both Schools'],
                            application__school_year=year,
                            ).values_list('address__city', flat=True).distinct()
    cities = list(set([city.title().strip() for city in list(cities)]))

    grades = ['6', '7', '8', '9', '10']
    result = {}

    for city in cities:
        counts_for_city = []

        for grade in grades:
            grade_count = Applicant.objects.filter(
                                    application__school__in=[school, 'Both Schools'],
                                    application__school_year=year,
                                    address__city__iexact=city,
                                    application__grade=grade
                                    ).values('application__grade').annotate(total=Count('application__grade'))
            if(grade_count):
                counts_for_city.append(grade_count[0]['total'])
            else:
                counts_for_city.append(0)

            result[city] = counts_for_city

    return result


def process_forms(forms):
    applicant = forms[0].save(commit=False)
    first_name = applicant.first_name.title()
    last_name = applicant.last_name.title()
    applicant.first_name = first_name
    applicant.last_name = last_name
    applicant.save()

    for form in forms[1:]:
        data = form.save(commit=False)
        data.applicant_id = applicant.pk
        data.save()


def no_previous_entry(applicant_data, application_data):
    applicant = Applicant.objects.filter(
                            first_name__iexact=applicant_data.get('first_name'),
                            last_name__iexact=applicant_data.get('last_name'),
                            date_of_birth=applicant_data.get('date_of_birth'),
                            application__school_year=application_data.get('school_year'),
                            application__school=application_data.get('school'),
                            ).first()
    return applicant == None

def are_all_valid(forms):
    are_valid_forms = [form.is_valid() for form in forms]
    return all(are_valid_forms)


def forms_data(forms):
    data = []
    for form in forms:
        data.append(form.cleaned_data)
    return data


def send_duplicate_entry_email(applicant_data, primary_parent_data):
    send_mail(
        'Duplicate Entry',
        f'''Dear {primary_parent_data.get('name')},\n\n
Our records indicate that there is already an application for \
{applicant_data.get('first_name')} {applicant_data.get('last_name')}.\n
Please contact our main office if you think there is a mistake.\n\n
Thank you
        ''',
        'mpolatpy@gmail.com',
        [primary_parent_data.get('email')],
        fail_silently=False,
    )

def send_confirmation_email(applicant_data, primary_parent_data):
    send_mail(
        'Application Confirmation',
        f'''Dear {primary_parent_data.get('name')},\n
We have successfully received the application for \
{applicant_data.get('first_name')} {applicant_data.get('last_name')}. \
You will receive your lottery number and other details in another email before the lottery.\n
Please contact our main office if you have any questions.\n
Thank you
        ''',
        'mpolatpy@gmail.com',
        [primary_parent_data.get('email')],
        fail_silently=False,
    )
