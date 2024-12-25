from django.shortcuts import render

from .models import Ticket


def index(request):
    template_name = 'tickets/index.html'
    # Возьмём нужное. А ненужное не возьмём:
    ticket_list = Ticket.objects.values(
        'id', 'departure', 'destination',
        'description', 'transcribed_destination',
    )
    context = {
        'ticket_list': ticket_list,
    }
    return render(request, template_name, context)
