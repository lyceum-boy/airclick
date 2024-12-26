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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, username=self.request.user.username)
        purchase_history = PurchaseHistory.objects.filter(user=profile).order_by('-purchased_at')
        context['purchase_history'] = purchase_history
        return context


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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart


@login_required
def cart_view(request):
    """Отображение содержимого корзины"""
    # Получаем корзину текущего пользователя
    cart_items = Cart.objects.filter(user=request.user)

    # Обрабатываем действия пользователя
    if request.method == "POST":
        action = request.POST.get("action")
        cart_item_id = request.POST.get("cart_item_id")
        cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)

        if action == "update_quantity":
            # Обновляем количество билетов
            new_quantity = int(request.POST.get("quantity", 1))
            cart_item.quantity = max(1, new_quantity)  # Убедимся, что количество >= 1
            cart_item.save()
        elif action == "remove":
            # Удаляем билет из корзины
            cart_item.delete()

        return redirect("tickets:cart_view")

    # Вычисляем общую стоимость
    total_price = sum(item.ticket.price * item.quantity for item in cart_items)

    return render(request, "tickets/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
    })


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Ticket, Cart


@login_required
def add_to_cart(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Проверяем, есть ли уже такой билет в корзине для текущего пользователя
    cart_item, created = Cart.objects.get_or_create(
        user=request.user, ticket=ticket,
        defaults={'quantity': 1}
    )

    if not created:
        # Если билет уже есть, увеличиваем количество
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Билет на рейс {ticket.departure} → {ticket.destination} добавлен в корзину.")

    # Перенаправляем на страницу корзины или на страницу с деталями билета
    return redirect('tickets:cart_view')  # Замените на нужный URL


from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Cart, PurchaseHistory


@login_required
def checkout(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)

        # Проверяем, есть ли товары в корзине
        if not cart_items:
            messages.error(request, "Ваша корзина пуста.")
            return redirect('tickets:cart_view')

        # Создаём записи в истории покупок
        for item in cart_items:
            PurchaseHistory.objects.create(
                user=request.user,
                ticket=item.ticket,
                total_price=item.ticket.price * item.quantity,
                purchased_at=timezone.now()
            )

        # Очистка корзины
        cart_items.delete()

        # Сообщение об успешной оплате
        messages.success(request, "Оплата успешно завершена. Ваши билеты добавлены в историю покупок.")

        return redirect('tickets:payment_success')  # Перенаправляем на страницу "Оплата успешно завершена"
    else:
        return redirect('tickets:cart_view')  # В случае некорректного запроса


@login_required
def payment_success(request):
    return render(request, 'tickets/success.html')
