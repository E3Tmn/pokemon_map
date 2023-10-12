# Generated by Django 3.1.14 on 2023-10-12 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0009_auto_20231012_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_evolutions', to='pokemon_entities.pokemon', verbose_name='Из кого эволюционировал'),
        ),
    ]
