from django import forms
from models import *

MAX_UPLOAD_SIZE = 2500000


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['last_name',
                  'first_name',
                  'middle_name',
                  'email',
                  'phone',
                  'address',
                  'date_of_birth',
                  'gender',
                  'ssn']

    Username = forms.CharField(max_length=20)
    Password = forms.CharField(max_length=200,
                               widget=forms.PasswordInput())
    Password2 = forms.CharField(max_length=200,
                                label="Confirm Password",
                                widget=forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('Password')
        password2 = cleaned_data.get('Password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_Username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('Username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username