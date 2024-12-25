from django.shortcuts import get_object_or_404, render

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


def ticket_detail(request, pk):
    template_name = 'tickets/detail.html'
    ticket = get_object_or_404(Ticket.objects.all(), pk=pk)
    context = {
        'ticket': ticket,
    }
    return render(request, template_name, context)
