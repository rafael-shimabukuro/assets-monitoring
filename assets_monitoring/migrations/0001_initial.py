# Generated by Django 4.2.4 on 2023-09-09 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10, unique=True)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('update_interval_minutes', models.PositiveIntegerField(default=10)),
                ('last_update', models.DateTimeField(null=True)),
                ('next_update', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetOwnership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('update_interval_minutes', models.PositiveIntegerField(default=10)),
                ('notified_date', models.DateField()),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets_monitoring.asset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='users',
            field=models.ManyToManyField(through='assets_monitoring.AssetOwnership', to=settings.AUTH_USER_MODEL),
        ),
    ]