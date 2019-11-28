from django.db import models
from django.contrib.auth.models import User


class Calculation(models.Model):
    functions = (
        ('loss_sphere', 'sphere'),
        ('loss_step', 'step'),
        ('loss_rastrigin', 'rastrigin'),
        ('loss_rosenbrock', 'rosenbrock')
    )
    function = models.CharField(choices=functions, verbose_name='Функция', max_length=15, blank=False)
    param_1 = models.FloatField(verbose_name='Дальность зрения', blank=False)
    param_2 = models.FloatField(verbose_name='Длина шага', blank=False)
    param_3 = models.FloatField(verbose_name='Дельта', blank=False)
    param_4 = models.IntegerField(verbose_name='Количество попыток', blank=False)
    user = models.ManyToManyField(User, verbose_name='Пользователь')
    minima_loss_1 = models.FloatField(verbose_name='Минимум 1', blank=False)
    minima_loss_2 = models.FloatField(verbose_name='Минимум 2', blank=False)
