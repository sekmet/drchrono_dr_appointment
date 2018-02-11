from django import forms
from django.contrib.auth import get_user_model

# forms go here
User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your full name"}
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your email"}
        )
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your message'
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print(str(email))
        if "gmail.com" not in email:
            raise forms.ValidationError("Email has to be gmail")
        return email

class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget= forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "Your email"}
    ))
    password = forms.CharField(widget= forms.PasswordInput(
        attrs={
                "class": "form-control",
                "placeholder": "Your password"}
    ),
        required=True)

    def clean_email(self):
        username = self.cleaned_data.get("email")
        print(str(username))
        if "@" not in username:
            raise forms.ValidationError("User name should be email")
        return username

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=255, required=True, widget= forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Your first name"}
    ))
    last_name = forms.CharField(max_length=255, required=True, widget= forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Your last name"}
    ))
    date_of_birth = forms.DateField(required=True,widget=forms.DateInput(
            attrs={
                "type":"date",
                "class": "form-control",
                "placeholder": "Your first name"}
        ))
    gender = forms.CharField(required=True, widget= forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Male/Female"}
    ))
    email    = forms.EmailField(required=True, widget= forms.EmailInput(
        attrs={
            "class": "form-control",
            "placeholder": "Your email"}
    ))
    home_phone = forms.DecimalField(required=False, widget= forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "0123456789"}
    ))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Your password"}
    ))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm password"}
    ))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is taken")
        return email

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if gender not in ['Male', 'Female', 'Other']:
            raise forms.ValidationError("Email is taken")
        return gender

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            raise forms.ValidationError("Password does not match")
        return  data

class JoinQueueForm(forms.Form):
    symptoms = forms.CharField(widget= forms.TextInput(
        attrs={
            "class": "form-control",
            "id" :"sympton-queue",
            "placeholder": "Please explain your symptoms"}
    ))


class AppointmentForm(forms.Form):
    symptoms = forms.CharField( widget= forms.TextInput(
        attrs={
            "class": "form-control",
            "id" :"sympton-appointment",
            "placeholder": "Please explain your symptoms"}
    ))
    time = forms.DateTimeField(widget=forms.DateTimeInput(
            attrs={
                "type":"datetime-local",
                "class": "form-control",
                "id": "time-to-visit",
                "placeholder": "Please enter your visit time"}
        ))

# class ="form-control" type="text" name="sympton" id="sympton-appointment" placeholder="Please explain your sympton" > < br >
# class ="form-control" type='datetime-local' name="time" id="time-to-visit" placeholder="Please enter your time" > < br >



