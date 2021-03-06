# Generated by Django 3.0.9 on 2020-08-04 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('refiner', '0001_initial'),
        ('intent_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.CharField(max_length=100)),
                ('cost_profile', models.CharField(max_length=100)),
                ('timeframe_start', models.CharField(default='00.00', max_length=100)),
                ('timeframe_end', models.CharField(default='00.00', max_length=100)),
                ('interval', models.CharField(max_length=100)),
                ('threshold', models.FloatField(default=0)),
                ('split_txs', models.BooleanField(default=False)),
                ('blockchain_pool', models.BinaryField(max_length=300)),
                ('blockchain_type', models.CharField(max_length=100)),
                ('min_tx_rate', models.IntegerField(default=4)),
                ('max_block_time', models.IntegerField(default=600)),
                ('min_data_size', models.IntegerField(default=20)),
                ('max_tx_cost', models.FloatField(default=0)),
                ('min_popularity', models.FloatField(default=0)),
                ('min_stability', models.FloatField(default=0)),
                ('turing_complete', models.BooleanField(default=False)),
                ('encryption', models.BooleanField(default=False)),
                ('redundancy', models.BooleanField(default=False)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='refiner.Currency')),
                ('intent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intent_manager.Intent')),
            ],
        ),
    ]
