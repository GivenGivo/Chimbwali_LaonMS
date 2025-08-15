from django import forms
from .models import Client
from django.contrib.auth import get_user_model

User = get_user_model()

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'full_name',
            'nrc',
            'phone_number',
            'passport_photo',
            'signature',
            'business_name',
            'address',
            'marital_status',
            'relationship_with_witness',
            'surety_name',
            'surety_value',
            'surety_make',
            'witness_name',
            'witness_nrc',
            'witness_phone',
        ]

class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'full_name',
            'nrc',
            'phone_number',
            'passport_photo',
            'signature',
            'business_name',
            'address',
            'marital_status',
            'relationship_with_witness',
            'surety_name',
            'surety_value',
            'surety_make',
            'witness_name',
            'witness_nrc',
            'witness_phone',
        ]

class ClientFilterForm(forms.Form):
    officer = forms.ChoiceField(
        required=False,
        label="Filter by Loan Officer",
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        officers = User.objects.filter(role='OFFICER').order_by('username')
        choices = [('', 'All Officers')] + [(str(officer.id), officer.get_full_name() or officer.username) for officer in officers]
        self.fields['officer'].choices = choices


from .models import TermsAndConditions, DailyReport, Announcement
from django import forms
from users.models import User

class LoanOfficerEditProfileForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900'
            }),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            # Add any password validation here if needed
            return password
        return None

class CEOEditProfileForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900'
            }),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return password
        return None

class LoanOfficerCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = 'OFFICER'
        user.is_active = True
        user.is_staff = False
        if commit:
            user.save()
        return user

class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = [
            'date',
            'total_expected',
            'total_collected',
            'advance_payments',
            'balance',
            'accumulative_balance',
            'clients_owing',
            'optional_note',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'optional_note': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add any additional comments (optional)...'
            }),
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter announcement title',
                'class': 'w-full rounded-xl border border-gray-300 dark:border-gray-600 px-4 py-3 bg-white dark:bg-surface-dark text-gray-900 dark:text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-primary'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Write your announcement...',
                'class': 'w-full rounded-xl border border-gray-300 dark:border-gray-600 px-4 py-3 bg-white dark:bg-surface-dark text-gray-900 dark:text-white shadow-sm focus:outline-none focus:ring-2 focus:ring-primary resize-y min-h-[150px]'
            }),
        }

class TermsAndConditionsForm(forms.ModelForm):
    class Meta:
        model = TermsAndConditions
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full h-80 p-4 border rounded-lg text-gray-800 dark:text-gray-200 bg-white dark:bg-gray-900 border-gray-300 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter the full terms and conditions...'
            }),
        }
