# Generated by Django 3.1.1 on 2020-12-05 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_dimtickers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EtfDailyQuote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('category', models.CharField(max_length=25)),
                ('closing_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='FuturesDailyQuote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('category', models.CharField(max_length=25)),
                ('contango', models.IntegerField()),
                ('front_contango', models.FloatField()),
                ('closing_price_1', models.FloatField()),
                ('closing_price_2', models.FloatField()),
                ('closing_price_3', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='quote',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='contents',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='creator_id',
        ),
        migrations.DeleteModel(
            name='DimTickers',
        ),
        migrations.RenameField(
            model_name='ticker',
            old_name='symbol',
            new_name='ticker_type',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='followed_watchlists',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='primary_watchlist',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='dep_tickers',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='description',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='parent_tickers',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='type',
        ),
        migrations.AddField(
            model_name='ticker',
            name='exchange',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='leverage_ratio',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='link',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='num_contracts',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='ticker_name',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.DeleteModel(
            name='Quote',
        ),
        migrations.DeleteModel(
            name='TickerType',
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
        migrations.AddField(
            model_name='futuresdailyquote',
            name='ticker_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ticker'),
        ),
        migrations.AddField(
            model_name='etfdailyquote',
            name='ticker_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ticker'),
        ),
        migrations.AddField(
            model_name='profile',
            name='followed_categories',
            field=models.ManyToManyField(blank=True, related_name='following', to='main.Category'),
        ),
        migrations.AddField(
            model_name='ticker',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.category'),
        ),
    ]
