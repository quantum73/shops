from django.core.validators import MinValueValidator
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=128, verbose_name='city_name')

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=128, verbose_name='street_name')

    class Meta:
        verbose_name = 'улица'
        verbose_name_plural = 'улицы'

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=128, verbose_name='shop_name')
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE,
        related_name='shop',
        verbose_name='shop_city'
    )
    street = models.ForeignKey(
        'Street',
        on_delete=models.CASCADE,
        related_name='shop',
        verbose_name='shop_street'
    )
    house_num = models.IntegerField(
        verbose_name='house_number',
        validators=[MinValueValidator(1)]
    )
    open_time = models.TimeField(verbose_name='open_time')
    close_time = models.TimeField(verbose_name='close_time')

    class Meta:
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'

    def __str__(self):
        return self.name
