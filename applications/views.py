from django.shortcuts import render, redirect, HttpResponse
from .forms import (ApplicationForm, ApplicantForm,PrimaryParentForm,
                    SecondaryParentForm, AddressForm, ReportForm, LotteryDataForm)
from .models import (Application, Applicant, PrimaryParent, SecondaryParent,
                    Address)
from django.views.generic import ListView, DetailView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test,login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import JsonResponse
import json
from .utils import (send_confirmation_email, process_forms, no_previous_entry,
                    are_all_valid, forms_data, get_application_counts, get_application_data)

def home(request):
    return render(request, 'applications/layout.html')

@login_required
def applicant_detail(request, pk):
    applicant = Applicant.objects.filter(pk=pk).first()
    # primary_parent = PrimaryParent.objects.filter(applicant=applicant).first()
    primary_parent = applicant.primaryparent_set.first()
    application = applicant.application_set.first()
    try:
        address = applicant.address_set.first()
    except:
        address = None
    secondary_parent = applicant.secondaryparent_set.first()

    if request.method == 'POST':
        form1 = ApplicantForm(request.POST, instance=applicant)
        form2 = ApplicationForm(request.POST, instance=application)
        form3 = PrimaryParentForm(request.POST, instance=primary_parent)
        form4 = SecondaryParentForm(request.POST, instance=secondary_parent)
        form5 = AddressForm(request.POST, instance=address)

        forms = [form1, form2, form3, form4, form5]

        if are_all_valid(forms):
            for form in forms:
                form.save()
            messages.success(request, 'Application details updated.')
            return redirect(request.path_info)
    else:
        form1 = ApplicantForm(instance=applicant)
        form2 = ApplicationForm(instance=application)
        form3 = PrimaryParentForm(instance=primary_parent)
        form4 = SecondaryParentForm(instance=secondary_parent)
        form5 = AddressForm(instance=address)

    context = {'applicant':applicant, 'form1':form1, 'form2':form2,
                'form3':form3, 'form4':form4, 'form5':form5}

    return render(request, 'applications/applicant.html', context)

def application_api(request):
    #doesn't work. Need to serialize data for JsonResponse
    if request.method == 'POST':
        school = request.POST['school']
        school_year = request.POST['school_year']
        grade = request.POST['grade']
        print(school, school_year, grade)
        queryset = Application.objects.filter(school=school)\
                                      .values('id', 'school', 'grade',
                                            'applicant__first_name', 'school_year',
                                            'applicant__last_name', 'applicant__pk')
        if queryset:
            return JsonResponse(json.dumps(list(queryset)), safe=False)
        return JsonResponse(data={})
    else:
        return render(request, 'applications/applications_api.html')

class ApplicationList(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications/applications.html'
    context_object_name = 'applications'
    # paginate_by = 8
    queryset = Application.objects.all()\
                                  .values('id', 'school', 'grade', 'application_date',
                                            'applicant__first_name', 'school_year',
                                            'applicant__last_name', 'applicant__pk')\
                                  .order_by('school_year', 'school', 'grade', 'applicant__last_name')

@login_required
def lottery(request):
    if request.method == 'POST':
        form = LotteryDataForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            data = json.loads(form_data['lotterydata'])
            ids = [app['id'] for app in data]
            applicants = Applicant.objects.filter(id__in=ids)
            for applicant in applicants:
                applicant.lottery_status = 'Waitlist'
                applicant.save()
            return render(request, 'applications/lottery_success.html', {'data': data, 'applicants':applicants})
        else:
            error = "Something went wrong!"
            return render(request, 'applications/lottery_fail.html', {'error': error})
    else:
        form = LotteryDataForm()
        applications = Applicant.objects.all()\
                          .values('id', 'application__school', 'application__grade', 'has_sibling',
                                    'first_name', 'application__school_year',
                                    'last_name', 'address__city')\
                          .order_by('application__school_year', 'application__school', 'application__grade','last_name')
        application_list = json.dumps(list(applications))
        return render(request, 'applications/lottery.html', {'application_list': application_list, 'form':form})

# class Lottery(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         form = LotteryDataForm()
#         return render(request, 'applications/lottery.html', {'application_list': self.get_context_data(), 'form':form})
#
#     def post(self, request, *args, **kwargs):
#         form = LotteryDataForm(request.POST)
#         error = None
#         if form.is_valid():
#             data = form.cleaned_data['lotterydata']
#             return render(request, 'applications/lottery_success.html', {'data': data, 'error': error})
#
#         error = "Form is not valid"
#         return render(request, 'applications/lottery_success.html', {'data': data, 'error': error})
#
#     def get_context_data(self, **kwargs):
#         applications = Applicant.objects.all()\
#                           .values('id', 'application__school', 'application__grade', 'has_sibling',
#                                     'first_name', 'application__school_year',
#                                     'last_name', 'address__city')\
#                           .order_by('application__school_year', 'application__school', 'application__grade','last_name')
#         application_list = json.dumps(list(applications))
#         return application_list

def application_form(request):
    if request.method == 'POST':
        form1 = ApplicantForm(request.POST)
        form2 = ApplicationForm(request.POST)
        form3 = PrimaryParentForm(request.POST)
        form4 = SecondaryParentForm(request.POST)
        form5 = AddressForm(request.POST)

        forms = [form1, form2, form3, form4, form5]

        if are_all_valid(forms):
            data = forms_data(forms)
            if no_previous_entry(data[0], data[1]):
                process_forms(forms)
                send_confirmation_email(data[0], data[2])
                return render(request, 'applications/application_success.html')
            else:
                applicant_info = data[0]
                application_info = data[1]
                return render(request, 'applications/application_failure.html',
                            {'applicant_info': applicant_info, 'application_info': application_info})
    else:
        form1 = ApplicantForm()
        form2 = ApplicationForm()
        form3 = PrimaryParentForm()
        form4 = SecondaryParentForm()
        form5 = AddressForm()

    return render(request, 'applications/application_form.html',
                            {'form1':form1, 'form2':form2,'form3':form3,
                            'form4':form4, 'form5':form5})


class ApplicantDelete(LoginRequiredMixin, DeleteView):
    model = Applicant
    success_url = reverse_lazy('application_list')
    success_message = f"Application was deleted successfully"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message)
        return super(ApplicantDelete, self).delete(request, *args, **kwargs)

@login_required
def application_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            school_year = form_data['school_year']
            school = form_data['school']
            application_data = json.dumps(get_application_counts(school, school_year))

            return render(request, 'applications/report.html',
                        {'application_data':application_data, 'form':form})
    else:
        form = ReportForm()
        return render(request, 'applications/request_report.html', {'form':form})
