from django import forms

from employers.models import EmployerProfile

from .models import CustomUser


class BasicProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'gender', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'gender': forms.RadioSelect(choices=CustomUser.GENDER_CHOICES),
            'role': forms.RadioSelect(choices=[('seeker', 'Job Seeker'), ('employer', 'Employer')]),
        }

    def clean_username(self):
        username = self.cleaned_data['username'].strip().lower().replace(' ', '_')
        exists = CustomUser.objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists()
        if exists:
            raise forms.ValidationError('This username is already taken.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        user.role = role
        user.is_employer = (role == 'employer')
        if commit:
            user.save()
        return user


class JobSeekerOnboardingForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['job_title', 'location', 'cv_file']
        widgets = {
            'job_title': forms.TextInput(attrs={'placeholder': 'e.g. Frontend Developer'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Cairo, Egypt'}),
        }


class EmployerOnboardingForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = [
            'company_name',
            'industry',
            'location',
            'description',
            'website',
            'position',
            'avatar_image',
            'banner_image',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Company name'}),
            'industry': forms.TextInput(attrs={'placeholder': 'e.g. Software, Healthcare'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Cairo, Egypt'}),
            'description': forms.Textarea(attrs={'placeholder': 'Tell candidates what your company does', 'rows': 5}),
            'website': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'position': forms.TextInput(attrs={'placeholder': 'Your position at the company'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['company_name', 'industry', 'location', 'description', 'position']:
            self.fields[field_name].required = True
        for field_name in ['website', 'avatar_image', 'banner_image']:
            self.fields[field_name].required = False
