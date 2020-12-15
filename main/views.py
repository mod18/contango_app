import datetime

from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from main.models import Category, Ticker, Profile


def welcome(request):
    """Defines view for welcome page."""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'welcome.html')


@login_required()
def home(request):
    """Defines view for user home page."""
    context = {}
    return render(request, 'main/home.html', context=context)


@login_required()
def ticker_detail(request, ticker_name):
    """Defines view for ticker detail page."""
    ticker = get_object_or_404(Ticker, ticker_name=ticker_name.upper())

    if ticker.ticker_type == 'ETF':
        recent_quotes = ticker.get_quotes()
        price_dates = [str(quote.date) for quote in recent_quotes]
        price_history = [str(quote.closing_price) for quote in recent_quotes]

        context = {
            'ticker': ticker,
            'price_dates': price_dates[::-1],
            'price_history': price_history[::-1],
        }
    elif ticker.ticker_type == 'Future':
        recent_quotes = ticker.get_futures_data()
        price_dates = [str(quote.date) for quote in recent_quotes]
        price_history = {'c1': [], 'c2': [], 'c3': []}
        for quote in recent_quotes:
            price_history['c1'].append(str(quote.closing_price_1))
            price_history['c2'].append(str(quote.closing_price_2))
            price_history['c3'].append(str(quote.closing_price_3))

        context = {
            'ticker': ticker,
            'price_dates': price_dates[::-1],
            'price_history_1': price_history['c1'][::-1],
            'price_history_2': price_history['c2'][::-1],
            'price_history_3': price_history['c3'][::-1],
        }
    else:
        context = {
            'ticker': ticker,
        }
    return render(request, 'main/ticker_detail.html', context=context)


@login_required()
def category_detail(request, category_name):
    """Defines view for category detail page."""
    category = get_object_or_404(Category, category_name=category_name.capitalize())
    user_followed_categories = request.user.profile.followed_categories.all()
    etfs = category.get_etfs()
    futures_contract = category.get_futures_contract()
    latest_futures_quote = futures_contract.get_latest_quote()
    futures_time_series = [
        str(latest_futures_quote.closing_price_1),
        str(latest_futures_quote.closing_price_2),
        str(latest_futures_quote.closing_price_3),
    ]
    context = {
        'category': category,
        'etfs': etfs,
        'futures_contract': futures_contract,
        'futures_time_series': futures_time_series,
        'user_followed_categories': user_followed_categories,
    }
    return render(request, 'main/category_detail.html', context)


@login_required()
def manage_categories(request):
    """Defines view to for a user to manage which categories they're following."""
    followed_categories = request.user.profile.followed_categories.all()

    context = {
        'followed_categories': followed_categories,
    }
    return render(request, 'main/manage_categories.html', context=context)


def follow_unfollow_category(request):
    """Handles logic for follow/unfollowing a category."""
    if request.method == "POST":
        user_profile = Profile.objects.get(user=request.user)
        category_pk = request.POST.get('category_pk')
        category = Category.objects.get(pk=category_pk)

        if category in user_profile.followed_categories.all():
            user_profile.followed_categories.remove(category)
        else:
            user_profile.followed_categories.add(category)
        return redirect(category.get_absolute_url())
    return redirect('home')


"""
Below are some generic editing views used to create, edit, and delete Author objects based on the Author model.

These views are a shortcut to create simple, standard views (and forms) really easily.

The default template names used will be <model_name>_form.html for the CreateView and UpdateView,
and will be <model_name>_confirm_delete.html for the DeleteView.
"""
class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = '__all__'


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = '__all__'


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('home')
































