from django.conf import settings
from django.db import models

STRING_MAX_LENGTH = 256  # Ограничение длины строки полей CharField.


class Ticket(models.Model):
    """Направление."""

    departure = models.CharField('Отправка', max_length=STRING_MAX_LENGTH)
    destination = models.CharField('Прибытие', max_length=STRING_MAX_LENGTH)
    description = models.TextField('Описание')
    airline = models.CharField('Авиакомпания', max_length=STRING_MAX_LENGTH)
    price = models.PositiveBigIntegerField('Стоимость билета')
    duration = models.PositiveSmallIntegerField('Продолжительность полёта')
    meals_on_board = models.BooleanField('Питание на борту')
    transcribed_destination = models.CharField(
        'Прибытие (англ.)', max_length=STRING_MAX_LENGTH
    )

    class Meta:
        verbose_name = 'билет'
        verbose_name_plural = 'Билеты'

    def __str__(self):
        return f'{self.departure} → {self.destination}'


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Пользователь"
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Билет"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")

    def __str__(self):
        return f"{self.user.username} - {self.ticket}"

    class Meta:
        verbose_name = "корзина"
        verbose_name_plural = "Корзины"


class PurchaseHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="purchase_history",
        verbose_name="Пользователь"
    )
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="Билет"
    )
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")

    def __str__(self):
        return f"{self.user.username} - {self.ticket}"

    class Meta:
        verbose_name = "История покупки"
        verbose_name_plural = "История покупок"
