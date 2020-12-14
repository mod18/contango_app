from django.contrib import admin
from .models import Profile, Category, Ticker, FuturesDailyQuote, EtfDailyQuote

@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'ticker_name',
        'category',
        'ticker_type',
        'link',
        'exchange',
        'num_contracts',
        'leverage_ratio',
    ]

@admin.register(FuturesDailyQuote)
class FuturesQuoteAdmin(admin.ModelAdmin):
    """All fields are visible, but none are editable."""
    list_display = [
        "ticker",
        "date",
        "contango",
        "front_contango",
        "closing_price_1",
        "closing_price_2",
        "closing_price_3",
    ]
    readonly_fields = list_display


@admin.register(EtfDailyQuote)
class EtfQuoteAdmin(admin.ModelAdmin):
    """All fields are visible, but none are editable."""
    list_display = [
        "ticker",
        "date",
        "closing_price",
    ]
    readonly_fields = list_display

admin.site.register(Profile)
admin.site.register(Category)
