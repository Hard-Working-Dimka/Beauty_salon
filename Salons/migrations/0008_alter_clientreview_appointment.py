# Generated by Django 4.2 on 2025-06-29 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Salons', '0007_alter_appointment_specialist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientreview',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Salons.appointment', verbose_name='client_reviews'),
        ),
    ]
