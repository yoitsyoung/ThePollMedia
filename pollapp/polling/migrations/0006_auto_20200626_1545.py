# Generated by Django 3.0.6 on 2020-06-26 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0005_auto_20200625_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='options', to='polling.Question'),
        ),
    ]
