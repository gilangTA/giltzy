# Generated by Django 3.2.4 on 2021-11-11 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knn_model', '0003_auto_20211026_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Knn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('performance', models.CharField(max_length=500)),
                ('analysis', models.CharField(max_length=5000)),
            ],
        ),
    ]
