from django import forms
from django.contrib.auth.models import User
from myapp.models import *
from django.contrib.auth.forms import AuthenticationForm

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['username', 'mobile_number', 'district', 'profile_picture', 'email']
        widgets = {
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        if username and email and password1:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user_profile.user = user
        if commit:
            user_profile.save()
        return user_profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class BathroomApplianceForm(forms.ModelForm):
    class Meta:
        model = BathroomAppliance
        fields = '__all__'
        widgets = {
            'bathroom_name': forms.TextInput(attrs={'class': 'form-control'}),
            'appliance_name': forms.TextInput(attrs={'class': 'form-control'}),
            'wattage': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'jan': forms.NumberInput(attrs={'class': 'form-control'}),
            'feb': forms.NumberInput(attrs={'class': 'form-control'}),
            'mar': forms.NumberInput(attrs={'class': 'form-control'}),
            'apr': forms.NumberInput(attrs={'class': 'form-control'}),
            'may': forms.NumberInput(attrs={'class': 'form-control'}),
            'jun': forms.NumberInput(attrs={'class': 'form-control'}),
            'jul': forms.NumberInput(attrs={'class': 'form-control'}),
            'aug': forms.NumberInput(attrs={'class': 'form-control'}),
            'sep': forms.NumberInput(attrs={'class': 'form-control'}),
            'oct': forms.NumberInput(attrs={'class': 'form-control'}),
            'nov': forms.NumberInput(attrs={'class': 'form-control'}),
            'dec': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class KitchenApplianceForm(forms.ModelForm):
    class Meta:
        model = KitchenAppliance
        fields = '__all__'
        widgets = {
            'kitchen_name': forms.TextInput(attrs={'class': 'form-control'}),
            'appliance_name': forms.TextInput(attrs={'class': 'form-control'}),
            'wattage': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'jan': forms.NumberInput(attrs={'class': 'form-control'}),
            'feb': forms.NumberInput(attrs={'class': 'form-control'}),
            'mar': forms.NumberInput(attrs={'class': 'form-control'}),
            'apr': forms.NumberInput(attrs={'class': 'form-control'}),
            'may': forms.NumberInput(attrs={'class': 'form-control'}),
            'jun': forms.NumberInput(attrs={'class': 'form-control'}),
            'jul': forms.NumberInput(attrs={'class': 'form-control'}),
            'aug': forms.NumberInput(attrs={'class': 'form-control'}),
            'sep': forms.NumberInput(attrs={'class': 'form-control'}),
            'oct': forms.NumberInput(attrs={'class': 'form-control'}),
            'nov': forms.NumberInput(attrs={'class': 'form-control'}),
            'dec': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BedroomApplianceForm(forms.ModelForm):
    class Meta:
        model = BedroomAppliance
        fields = '__all__'
        widgets = {
            'bedroom_name': forms.TextInput(attrs={'class': 'form-control'}),
            'appliance_name': forms.TextInput(attrs={'class': 'form-control'}),
            'wattage': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'jan': forms.NumberInput(attrs={'class': 'form-control'}),
            'feb': forms.NumberInput(attrs={'class': 'form-control'}),
            'mar': forms.NumberInput(attrs={'class': 'form-control'}),
            'apr': forms.NumberInput(attrs={'class': 'form-control'}),
            'may': forms.NumberInput(attrs={'class': 'form-control'}),
            'jun': forms.NumberInput(attrs={'class': 'form-control'}),
            'jul': forms.NumberInput(attrs={'class': 'form-control'}),
            'aug': forms.NumberInput(attrs={'class': 'form-control'}),
            'sep': forms.NumberInput(attrs={'class': 'form-control'}),
            'oct': forms.NumberInput(attrs={'class': 'form-control'}),
            'nov': forms.NumberInput(attrs={'class': 'form-control'}),
            'dec': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DininghallApplianceForm(forms.ModelForm):
    class Meta:
        model = DininghallAppliance
        fields = '__all__'
        widgets = {
            'dininghall_name': forms.TextInput(attrs={'class': 'form-control'}),
            'appliance_name': forms.TextInput(attrs={'class': 'form-control'}),
            'wattage': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'jan': forms.NumberInput(attrs={'class': 'form-control'}),
            'feb': forms.NumberInput(attrs={'class': 'form-control'}),
            'mar': forms.NumberInput(attrs={'class': 'form-control'}),
            'apr': forms.NumberInput(attrs={'class': 'form-control'}),
            'may': forms.NumberInput(attrs={'class': 'form-control'}),
            'jun': forms.NumberInput(attrs={'class': 'form-control'}),
            'jul': forms.NumberInput(attrs={'class': 'form-control'}),
            'aug': forms.NumberInput(attrs={'class': 'form-control'}),
            'sep': forms.NumberInput(attrs={'class': 'form-control'}),
            'oct': forms.NumberInput(attrs={'class': 'form-control'}),
            'nov': forms.NumberInput(attrs={'class': 'form-control'}),
            'dec': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class LivingroomApplianceForm(forms.ModelForm):
    class Meta:
        model = LivingroomAppliance
        fields = '__all__'
        widgets = {
            'livingroom_name': forms.TextInput(attrs={'class': 'form-control'}),
            'appliance_name': forms.TextInput(attrs={'class': 'form-control'}),
            'wattage': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'jan': forms.NumberInput(attrs={'class': 'form-control'}),
            'feb': forms.NumberInput(attrs={'class': 'form-control'}),
            'mar': forms.NumberInput(attrs={'class': 'form-control'}),
            'apr': forms.NumberInput(attrs={'class': 'form-control'}),
            'may': forms.NumberInput(attrs={'class': 'form-control'}),
            'jun': forms.NumberInput(attrs={'class': 'form-control'}),
            'jul': forms.NumberInput(attrs={'class': 'form-control'}),
            'aug': forms.NumberInput(attrs={'class': 'form-control'}),
            'sep': forms.NumberInput(attrs={'class': 'form-control'}),
            'oct': forms.NumberInput(attrs={'class': 'form-control'}),
            'nov': forms.NumberInput(attrs={'class': 'form-control'}),
            'dec': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        
