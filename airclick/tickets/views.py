from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import UserForm
from .models import Ticket

User = get_user_model()


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


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'
    template_name = 'tickets/profile.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.object
    #     posts = (
    #         Post.objects
    #         .annotate(comment_count=Count('comments'))
    #         .filter(author=user)
    #         .order_by('-pub_date')
    #     )
    #     paginator = Paginator(posts, 10)
    #     page_number = self.request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #     context['page_obj'] = page_obj
    #     return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'tickets/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'tickets:profile',
            kwargs={'username': self.request.user.username}
        )
