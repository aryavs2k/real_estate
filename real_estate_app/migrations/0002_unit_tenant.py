# Generated by Django 4.2.2 on 2024-01-04 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='tenant',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='real_estate_app.userdetails'),
            preserve_default=False,
        ),
    ]
