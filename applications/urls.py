from django.urls import path
from . import views as application_view
from .views import ApplicationList, applicant_detail, ApplicantDelete #Lottery

urlpatterns = [
    # path('application-list/', application_view.applications, name='application_list'),
    path('applicant/<int:pk>/', application_view.applicant_detail, name='applicant_detail'),
    path('application-list/', ApplicationList.as_view(), name='application_list'),
    path('application-api/', application_view.application_api, name='application_api'),
    path('application-form/', application_view.application_form, name='application_form'),
    path('application-report/', application_view.application_report, name='application_report'),
    path('applicant/<int:pk>/delete', ApplicantDelete.as_view(), name='applicant-delete'),
    path('lottery/', application_view.lottery, name='lottery'),
    # path('lottery/', Lottery.as_view(), name='lottery')
]
