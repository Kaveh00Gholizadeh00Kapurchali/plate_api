# Generated by Django 5.1.3 on 2024-12-11 17:04

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vehicle_plate', models.CharField(max_length=255, unique=True)),
                ('status', models.BooleanField(default=False)),
                ('image_url', models.URLField(blank=True, default='', null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='vehicle_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrafficHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(max_length=255)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traffic_history', to='plate_api.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField()),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='plate_api.vehicle')),
            ],
        ),
    ]
