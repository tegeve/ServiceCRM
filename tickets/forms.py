from django import forms
from django.contrib.auth.models import User
from . import models


class AgetUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class AgentForm(forms.ModelForm):
    class Meta:
        model = models.Agent
        fields = ['email', 'mobile']


class TehnicianUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class TehnicianForm(forms.ModelForm):
    class Meta:
        model = models.Tehnician
        fields = ['email', 'mobile', 'specializari']


class RequestForm(forms.ModelForm):
    class Meta:
        model = models.Request
        fields = ['category', 'reper_no', 'reper_name', 'reper_model', 'reper_brand', 'problem_description']
        widgets = {
            'problem_description': forms.Textarea(attrs={'rows': 3, 'cols': 30})
        }


class AdminRequestForm(forms.Form):
    # to_field_name value will be stored when form is submitted.....__str__ method of customer model will be shown
    # there in html
    customer = forms.ModelChoiceField(queryset=models.Agent.objects.all(), empty_label="Nume agent",
                                      to_field_name='id')
    mechanic = forms.ModelChoiceField(queryset=models.Tehnician.objects.all(), empty_label="Nume tehnician",
                                      to_field_name='id')
    cost = forms.IntegerField()


class AdminApproveRequestForm(forms.Form):
    mechanic = forms.ModelChoiceField(queryset=models.Tehnician.objects.all(), empty_label="Nume Tehnician",
                                      to_field_name='id')
    cost = forms.IntegerField()
    stat = (('In asteptare', 'In asteptare'), ('Aprobat', 'Aprobat'), ('Trimis', 'Trimis'))
    status = forms.ChoiceField(choices=stat)


class TehnicianSpecializeForm(forms.Form):
    specializare = forms.CharField()


class UpdateCostForm(forms.Form):
    cost = forms.IntegerField()


class TehnicianUpdateStatusForm(forms.Form):
    stat = (('Aprobat', 'Aprobat'), ('In reparatie', 'In reparatie'), ('Asteapta piese', 'Asteapta piese'), ('Reparat', 'Reparat'))
    status = forms.ChoiceField(choices=stat)


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = ['by', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }


# for Attendance related form
presence_choices = (('Prezent', 'Prezent'), ('Absent', 'Absent'))


class AttendanceForm(forms.Form):
    present_status = forms.ChoiceField(choices=presence_choices)
    date = forms.DateField()


class AskDateForm(forms.Form):
    date = forms.DateField()


# for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
