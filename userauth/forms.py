from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' , 'first_name', 'last_name', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['username'].widget.attrs.update({'class': 'w-full'})     
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full p-1'})

    