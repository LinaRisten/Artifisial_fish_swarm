from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from afs.models import Calculation
from afs.forms import AuthForm, CalculatorForm

from afs.afs import run


class LoginView(View):
    def get(self, request):
        form = AuthForm(request=request)
        context = {
            'form': form,
            'success_url': request.META.get('HTTP_REFERER', reverse('afs:calculator'))
        }
        return render(request, 'afs/login.html', context)

    def post(self, request):
        success_url = request.POST.get('success_url', reverse('afs:calculator'))

        form = AuthForm(request.POST, request=request)

        if form.is_valid():
            return HttpResponseRedirect(success_url)
        else:
            context = {
                'form': form,
                'success_url': success_url
            }
            return render(request, 'afs/login.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('afs:calculator')))


class CalculatorView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            calculations = Calculation.objects.all().order_by('pk')
        else:
            calculations = Calculation.objects.filter(user=request.user).order_by('pk')
        context = {
            'form': CalculatorForm(),
            'calculations': calculations
        }
        return render(request, 'afs/calculator.html', context)

    def post(self, request):
        user = request.user
        calculations = Calculation.objects.filter(user=user).order_by('pk')

        form = CalculatorForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            result = run(function=data['function'], param_1=data['param_1'], param_2=data['param_2'],
                         param_3=data['param_3'], param_4=data['param_4'])

            calculation = Calculation.objects.create(function=data['function'],
                                                     param_1=data['param_1'], param_2=data['param_2'],
                                                     param_3=data['param_3'], param_4=data['param_4'],
                                                     minima_loss_1=result['minima_loss_1'],
                                                     minima_loss_2=result['minima_loss_2'])
            calculation.user.set(User.objects.filter(id=request.user.id))

        else:
            context = {
                'form': form,
                'calculations': calculations
            }
            return render(request, 'afs/calculator.html', context)

        return HttpResponseRedirect(reverse('afs:calculator'))


class DeleteCalculationView(LoginRequiredMixin, View):
    def get(self, request, *_, **kwargs):
        Calculation.objects.get(pk=kwargs.get('calculation_id')).delete()
        return HttpResponseRedirect(reverse('afs:calculator'))
