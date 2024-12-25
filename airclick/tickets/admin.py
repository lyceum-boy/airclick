from django.contrib import admin

from .models import Ticket

admin.site.empty_value_display = 'Не задано'


@admin.register(Ticket)
class CategoryTicket(admin.ModelAdmin):
    list_display = (
        'departure',
        'destination',
        'description',
        'airline',
        'price',
        'duration',
        'meals_on_board',
        'transcribed_destination',
    )
    list_filter = ('meals_on_board',)
    list_display_links = ('destination',)
