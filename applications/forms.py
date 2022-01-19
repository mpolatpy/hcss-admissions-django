from django import forms
import json
from .models import (Application, Applicant, PrimaryParent,
                    SecondaryParent, Address, SchoolYear)

class ApplicantForm(forms.ModelForm):
    middle_name = forms.CharField(required=False)
    # middle_name.widget.attrs['class'] = 'form-control-sm'
    date_of_birth = forms.DateField(label='Date of birth',
                                    widget=forms.DateInput(attrs={'placeholder': 'mm-dd-yyyy'}),
                                    input_formats=['%m-%d-%Y', '%m/%d/%Y', '%Y-%m-%d', '%Y/%m/%d'])
    has_sibling = forms.ChoiceField(label = 'Does the applicant have a sibling* who currently attends HCSS?',
                               choices=[(True,'Yes'), (False, 'No')],
                               widget=forms.RadioSelect(attrs={'required':True}))
    lottery_status = forms.ChoiceField(choices=[
                                        ('Lottery', 'Lottery'),
                                        ('Waitlist', 'Waitlist'),
                                        ('Admitted', 'Admitted'),
                                        ('Registered', 'Registered'),
                                        ('Declined', 'Declined')
                                    ], required=False)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1}))

    class Meta:
        model = Applicant
        fields = ['first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender','current_school',
        'current_grade', 'has_sibling', 'sibling_name', 'sibling_grade', 'notes', 'lottery_status','waitlist_number']


class ApplicationForm(forms.ModelForm):
    school = forms.ChoiceField(label = 'To which school are you applying?',
                               choices=[('HCSS East','HCSS East'),
                                        ('HCSS West','HCSS West'),
                                        ('Both Schools', 'Both Schools')],
                                widget=forms.RadioSelect(attrs={'required':True}))
    school_years = SchoolYear.objects.filter(display_on_form=True)
    school_year = forms.ChoiceField(label = 'To which year are you applying?',
                                    choices=[(year.school_year, year.form_display_value) for year in school_years],
                                    widget=forms.RadioSelect(attrs={'required':True}))

    grade = forms.ChoiceField(label = 'To which grade are you applying?',
                                    choices=[('6', 'Grade 6'),
                                             ('7', 'Grade 7'),
                                             ('8', 'Grade 8'),
                                             ('9', 'Grade 9'),
                                             ('10', 'Grade 10'),],
                                    widget=forms.RadioSelect(attrs={'required':True}))

    how_did_you_hear = forms.ChoiceField(label = 'How did you hear about HCSS-East and/or HCSS-West?',
                               choices=[('Billboard','Billboard'),
                                        ('Facebook-Twitter', 'Facebook-Twitter'),
                                        ('Flyer-Brochure', 'Flyer-Brochure'),
                                        ('Library - Open Houses', 'Library - Open Houses'),
                                        ('Local Newspaper Ad', 'Local Newspaper Ad'),
                                        ('Poster', 'Poster'),
                                        ('Radio Ad', 'Radio Ad'),
                                        ('TV Ad', 'TV Ad'),
                                        ('Website-Search Engine', 'Website-Search Engine'),
                                        ('Yard Sign', 'Yard Sign'),
                                        ('Other', 'Other')],
                                widget=forms.RadioSelect(attrs={'required':True}))
    other_hear_option = forms.CharField(label='If other, please enter your answer here.', required=False)
    agree_to_terms = forms.BooleanField(label='I agree', required=True)

    class Meta:
        model = Application
        fields = ['school', 'school_year', 'grade', 'how_did_you_hear', 'other_hear_option', 'agree_to_terms']

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['address', 'city', 'state', 'zip_code']

class PrimaryParentForm(forms.ModelForm):

    class Meta:
        model = PrimaryParent
        fields = ['name', 'relation', 'email', 'phone_number']

class SecondaryParentForm(forms.ModelForm):

    secondary_parent_name = forms.CharField(label="Name", required=False)
    secondary_parent_relation = forms.CharField(label="Relation", required=False)
    secondary_parent_email = forms.EmailField(label="Email", required=False)
    secondary_parent_phone_number = forms.CharField(label="Phone Number", required=False)

    class Meta:
        model = SecondaryParent
        fields = ['secondary_parent_name', 'secondary_parent_relation', 'secondary_parent_email', 'secondary_parent_phone_number']


class ReportForm(forms.Form):

    school_year = forms.ChoiceField(label='', choices=[('', 'School Year'), ('21-22', '21-22'),('20-21', '20-21')])
    school = forms.ChoiceField(label='', choices=[('', 'School'),('HCSS East', 'HCSS East'),('HCSS West', 'HCSS West')])

class LotteryDataForm(forms.Form):

    lotterydata = forms.CharField()

    # def clean_lotterydata(self):
    #     data = self.cleaned_data['lotterydata']
    #     try:
    #         json_data = json.loads(data)
    #     except:
    #         raise forms.ValidationError('Invalid data')
    #
    #     return data
