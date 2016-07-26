# -*- coding: utf-8 -*-
from django import forms
from models import Track, Task, Researcher, Run
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class TaskForm(forms.ModelForm):
    track = forms.ModelChoiceField(queryset=Track.objects.all().order_by('track_title'))
    title = forms.CharField(max_length=32, label='Title:')
    description = forms.CharField(max_length=128, label='Description:')
    year = forms.CharField(max_length=4, validators=[RegexValidator(r'^\d{1,10}$')], label='Year:')
    judgement_file = forms.FileField(label='Judgement File:')

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Task
        fields = ('track', 'title', 'description', 'year', 'judgement_file',)  # Values that are written to in form


class TrackForm(forms.ModelForm):
    track_title = forms.CharField(max_length=32, label='Title:')
    description = forms.CharField(max_length=128, label='Description:')
    genre = forms.CharField(max_length=32, label='Genre:')

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Track
        fields = ('track_title', 'description', 'genre')


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(), required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Password")
    email = forms.EmailField(widget=forms.EmailInput(), required=True, label="Email")
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class ResearcherForm(forms.ModelForm):
    display_name = forms.CharField(max_length=16, label='Display name:')
    profile_picture = forms.ImageField(required=False, label='Profile Picture:')
    website = forms.URLField(max_length=128, label='Website:', required=False)
    organization = forms.CharField(max_length=64, label='Organization:', required=False)

    class Meta:
        model = Researcher
        fields = ("display_name", "profile_picture", "website", "organization",)


class UpdateProfile(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, label='Profile Picture:')
    website = forms.URLField(max_length=128, label='Website:', required=False)
    organization = forms.CharField(max_length=64, label='Organization:', required=False)
    
    class Meta:
        model = Researcher
        fields = ("profile_picture", "website", "organization",)
    
    
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Password")


class RunForm(forms.ModelForm):
    task = forms.ModelChoiceField(queryset=Task.objects.all().order_by('title'), label='Task:', required=True)
    name = forms.CharField(required=True, max_length=64, label='Run name:')
    description = forms.CharField(required=False, max_length=256, label='Description:')
    result_file = forms.FileField(required=True, label='Result File:')
    run_type = forms.ChoiceField(required=True, choices=Run.RUNCHOICES, label='Run type:')
    query_type = forms.ChoiceField(required=True, choices=Run.QUERYCHOICES,label='Query type:')
    feedback_type = forms.ChoiceField(required=True, choices=Run.FEEDBACKCHOICES, label='Feedback type:')

    class Meta:
        model = Run
        fields = ("task", "name", "description", "result_file", "run_type", "query_type", "feedback_type",)


