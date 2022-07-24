import datetime

from django.db import models

# Create your models here.


class BuyOrRentDeal(models.Model):

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    user_id = models.BigIntegerField(verbose_name='id пользователя')
    commercial_id = models.BigIntegerField(verbose_name='id помещения')
    price = models.BigIntegerField(verbose_name='стоимость')
    expires = models.DateField(verbose_name='дата аренды')
    deal_type = models.CharField(max_length=10, choices=[('1', 'Аренда'), ('2', 'Покупка')], verbose_name='тип сделки')
    date = models.DateField(auto_now=True, verbose_name='дата создания')
    status = models.CharField(max_length=15, verbose_name='статус',
                              choices=[('1', 'В обработке'), ('2', 'Отказ'), ('3', 'Принято')], default='1')

    def __str__(self):
        return f'Заявка №{self.pk} на {self.deal_type}'


class MarketplaceService(models.Model):
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    name = models.CharField(max_length=40, verbose_name='название услуги')
    image = models.ImageField(upload_to='images/', verbose_name='изображение')
    url = models.URLField(verbose_name='ссылка на компанию')
    descr = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.name
