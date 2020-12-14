# Generated by Django 3.1.1 on 2020-10-10 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('dep_tickers', models.ManyToManyField(blank=True, related_name='deps', to='main.Ticker')),
                ('parent_tickers', models.ManyToManyField(blank=True, related_name='parents', to='main.Ticker')),
            ],
        ),
        migrations.CreateModel(
            name='TickerType',
            fields=[
                ('type_id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=100)),
                ('sub_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watchlist_name', models.CharField(help_text='Enter a name for this watchlist', max_length=100)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
                ('contents', models.ManyToManyField(to='main.Ticker')),
                ('creator_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('followers', models.ManyToManyField(related_name='follower', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ticker',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.tickertype'),
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique id for this quote', primary_key=True, serialize=False)),
                ('price', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('data_source', models.CharField(max_length=250)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ticker')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_watchlist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.watchlist')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]