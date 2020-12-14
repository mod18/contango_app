from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse
import uuid


class Profile(models.Model):
    """Profile class.

    Adds a few extra features to the Django base User class.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followed_categories = models.ManyToManyField('Category', related_name='following', blank=True)

    def get_followed_categories(self):
        """Gets a list of all categories a user follows."""
        return self.followed_categories.all()
    get_followed_categories.short_description = 'Followed categories'

    def __str__(self):
        return f'{self.user.username} (Profile)'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    """Model for categories.

    Categories are collections of ETFs and related futures.
    """
    category_name = models.CharField(max_length=100)

    def get_tickers(self):
        return Ticker.objects.filter(category=self.id).all()

    def get_futures_contract(self):
        return Ticker.objects.get(category=self.id, ticker_type='Future')

    def get_etfs(self):
        return Ticker.objects.filter(category=self.id).filter(ticker_type='ETF').all()

    def tickers_count(self):
        return Ticker.objects.filter(category=self.id).count()

    def follower_count(self):
        return Profile.objects.filter(followed_categories=self.id).count()

    def get_followers(self):
        return Profile.objects.filter(followed_categories=self.id)

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.category_name)])

    def __str__(self):
        return f'{self.category_name} (Category)'


class Ticker(models.Model):
    """Model for futures/etf tickers

    """
    ticker_name = models.CharField(max_length=10, null=True)
    category = models.ForeignKey('Category', null=True, on_delete=models.CASCADE)
    ticker_type = models.CharField(max_length=10)
    link = models.CharField(max_length=100, null=True, blank=True)
    exchange = models.CharField(max_length=10, null=True, blank=True)
    num_contracts = models.IntegerField(null=True, blank=True)
    leverage_ratio = models.IntegerField(null=True, blank=True)

    def get_latest_quote(self):
        """Returns the most recent closing price for a ticker."""
        if self.ticker_type == 'ETF':
            return EtfDailyQuote.objects.filter(ticker=self.id).latest('date')
        elif self.ticker_type == 'Future':
            return FuturesDailyQuote.objects.filter(ticker=self.id).latest('date')
    get_latest_quote.short_description = 'Most recent quote'

    def get_latest_price_update_date(self):
        """Returns the most recent update date for a ticker."""
        if self.ticker_type == 'ETF':
            return EtfDailyQuote.objects.filter(ticker=self.id).latest('date').date
        elif self.ticker_type == 'Future':
            return FuturesDailyQuote.objects.filter(ticker=self.id).latest('date').date
    get_latest_price_update_date.short_description = 'Most recent update date'

    def get_quotes(self):
        """Returns a list of the 20 most recent quotes for a given ETF."""
        if self.ticker_type == 'ETF':
            return EtfDailyQuote.objects.filter(ticker=self.id).order_by('-date')[:20]

    def get_futures_data(self):
        """Returns the 20 most recent quotes for a given Future."""
        if self.ticker_type == 'Future':
            return FuturesDailyQuote.objects.filter(ticker=self.id).order_by('-date')[:20]

    def get_absolute_url(self):
        return reverse('ticker-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.ticker_name}'


class FuturesDailyQuote(models.Model):
    """Model for daily futures quote and related data."""
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    date = models.DateField()
    contango = models.IntegerField()
    front_contango = models.FloatField()
    closing_price_1 = models.FloatField()
    closing_price_2 = models.FloatField()
    closing_price_3 = models.FloatField()

    def is_contango(self):
        if self.contango == 1:
            return True
        else:
            return False

    def __str__(self):
        return f'Data for {self.ticker} on {self.date}'

    class Meta:
        db_table = 'fct_futures_daily'
        managed = False

class EtfDailyQuote(models.Model):
    """Model for daily ETF quote."""
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    date = models.DateField()
    closing_price = models.FloatField()

    def __str__(self):
        return f'Data for {self.ticker} on {self.date}'

    class Meta:
        db_table = 'fct_etf_daily'
        managed = False
