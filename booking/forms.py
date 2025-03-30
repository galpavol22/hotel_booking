from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    """
    Formulár pre registráciu používateľa, ktorý okrem užívateľského mena a hesla
    vyžaduje aj email a telefón. Heslo sa uloží s použitím hashovacieho algoritmu.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Telefón'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Heslo'})
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password"]

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
