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
