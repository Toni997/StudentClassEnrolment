# Generated by Django 4.0.4 on 2022-06-03 12:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predmeti', '0005_alter_predmeti_studenti'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predmeti',
            name='bodovi',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Predmet ne može nositi manje od jednog boda.')]),
        ),
    ]
