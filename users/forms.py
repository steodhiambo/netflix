from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    birth = forms.DateField(widget=DateInput, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birth')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"{username} is already taken.")
        return username

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data['email']
        user.save()
        customer = Customer.objects.create(user=user, birth=self.cleaned_data['birth'])
        return user


class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    field = forms.ChoiceField(choices=(
        ('Air Conditioner', 'Air Conditioner'),
        ('All in One', 'All in One'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('Housekeeping', 'Housekeeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters')
    ), required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'field')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"{username} is already taken.")
        return username

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.email = self.cleaned_data['email']
        user.save()
        company = Company.objects.create(user=user, field=self.cleaned_data['field'])
        return user


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Username or Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
