# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class ClosingQuotes(models.Model):
    type = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    ticker = models.TextField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    retrieved_ts = models.IntegerField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'closing_quotes'


class DimTickers(models.Model):
    ticker_name = models.TextField(primary_key=True, null=True)  # This field type is a guess.
    category = models.TextField(blank=True, null=True)
    ticker_type = models.TextField(blank=True, null=True)
    exchange = models.TextField(blank=True, null=True)
    num_contracts = models.IntegerField(blank=True, null=True)
    leverage_ratio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_tickers'




class FctClosingQuotesDaily(models.Model):
    date = models.TextField(blank=True, null=True)
    ticker_name = models.TextField(blank=True, null=True)
    ticker_contract = models.IntegerField(blank=True, null=True)
    closing_price = models.FloatField(blank=True, null=True)
    retrieved_ts = models.IntegerField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fct_closing_quotes_daily'


class FctClosingQuotesRaw(models.Model):
    date = models.TextField(blank=True, null=True)
    ticker_name = models.TextField(blank=True, null=True)
    ticker_contract = models.IntegerField(blank=True, null=True)
    closing_price = models.FloatField(blank=True, null=True)
    retrieved_ts = models.IntegerField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fct_closing_quotes_raw'


class FctContangoDaily(models.Model):
    date = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    ticker_name = models.TextField(blank=True, null=True)
    contango = models.IntegerField(blank=True, null=True)
    front_contango = models.FloatField(blank=True, null=True)
    closing_price_1 = models.FloatField(blank=True, null=True)
    closing_price_2 = models.FloatField(blank=True, null=True)
    closing_price_3 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fct_futures_daily'


class FctEtfDaily(models.Model):
    date = models.TextField(blank=True, null=True)
    ticker_name = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    closing_price = models.FloatField(blank=True, null=True)
    leverage_ratio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fct_etf_daily'


class Tickers(models.Model):
    category = models.TextField(blank=True, null=True)
    ticker_name = models.TextField(blank=True, null=True)
    ticker_type = models.TextField(blank=True, null=True)
    exchange = models.TextField(blank=True, null=True)
    num_contracts = models.IntegerField(blank=True, null=True)
    leverage_ratio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickers'
