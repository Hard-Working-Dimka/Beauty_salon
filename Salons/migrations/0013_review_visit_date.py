# Generated by Django 4.2 on 2025-07-01 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salons', '0012_alter_appointment_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='visit_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
