from django import forms
from django.contrib.auth import authenticate, login
from afs.models import Calculation


class AuthForm(forms.Form):
    login = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    def __init__(self, *_, **kwargs):
        self.request = kwargs.pop('request')
        super(AuthForm, self).__init__(*_, **kwargs)

    def clean(self, *_, **kwargs):
        username = self.cleaned_data['login']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user:
            login(self.request, user)
        else:
            raise forms.ValidationError(
                {'password': 'Неверные учетные данные'})


class CalculatorForm(forms.ModelForm):
    class Meta:
        model = Calculation
        exclude = ('user', 'minima_loss_1', 'minima_loss_2')
        verbose_name = 'Результат вычислений'
        verbose_name_plural = 'Результаты вычислений'
        widgets = {
            'minima_loss_1': forms.HiddenInput(),
            'minima_loss_2': forms.HiddenInput(),
            'param_1': forms.TextInput(attrs={'placeholder': '0.5'}),
            'param_2': forms.TextInput(attrs={'placeholder': '0.2'}),
            'param_3': forms.TextInput(attrs={'placeholder': '0.5'}),
            'param_4': forms.TextInput(attrs={'placeholder': '5'}),
        }
