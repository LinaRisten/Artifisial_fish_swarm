from django.db import models
from django.contrib.auth.models import User


class Calculation(models.Model):
    functions = (
        ('loss_sphere', 'loss sphere'),
        ('loss_step', 'loss step'),
        ('loss_rastrigin', 'loss rastrigin'),
        ('loss_rosenbrock', 'loss rosenbrock')
    )
    function = models.CharField(choices=functions, verbose_name='Метод', max_length=15, blank=False)
    param_1 = models.FloatField(verbose_name='1-ый параметр', blank=False)
    param_2 = models.FloatField(verbose_name='2-ый параметр', blank=False)
    param_3 = models.FloatField(verbose_name='3-ый параметр', blank=False)
    param_4 = models.IntegerField(verbose_name='4-ый параметр', blank=False)
    user = models.ManyToManyField(User, verbose_name='Пользователь')
    minima_loss_1 = models.FloatField(verbose_name='minima_loss_1', blank=False)
    minima_loss_2 = models.FloatField(verbose_name='minima_loss_2', blank=False)
