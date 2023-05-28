from django import forms
from django.contrib.auth.models import User
from .models import Song
from django.core.exceptions import ValidationError
 
# creating a validator function




class UserForm(forms.ModelForm):
    username = forms.EmailField(max_length=254,help_text="Please enter ur email address")
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password')
class songForm(forms.ModelForm):
    allowed_emails = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text="Enter multiple email addresses separated by commas (,)",
    )
    class Meta():
        model = Song
        fields = ['audio_name','audio_file','audio_type','allowed_emails']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['audio_file'].widget.attrs['accept'] = 'audio/*'
        self.fields['audio_name'].required = True
        self.fields['audio_file'].required = True
        self.fields['audio_type'].required = True

