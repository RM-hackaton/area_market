import datetime

from django.db import models

# Create your models here.


class BuyOrRentDeal(models.Model):
    user_id = models.BigIntegerField()
    commercial_id = models.BigIntegerField()
    price = models.BigIntegerField()
    expires = models.DateField()
    deal_type = models.CharField(max_length=10, choices=[('1', 'Аренда'), ('2', 'Покупка')])
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=15,
                              choices=[('1', 'В обработке'), ('2', 'Отказ'), ('3', 'Принято')], default='1')

    def __str__(self):
        return f'Заявка №{self.pk} на {self.deal_type}'


class MarketplaceService(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to='images/')
    url = models.URLField()
    descr = models.TextField()

    def __str__(self):
        return self.name
