# Generated by Django 4.0.4 on 2022-04-17 14:09

from django.db import migrations, models
import django.db.models.deletion
import restaurants.models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_rename_user_id_restaurant_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('photo', models.CharField(default='default.png', max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='photo',
            field=models.CharField(default='default.png', max_length=1000),
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr', models.CharField(auto_created=True, max_length=50, unique=True)),
                ('number', models.IntegerField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10000)),
                ('photo', models.CharField(blank=True, default='default.png', max_length=1000, null=True)),
                ('optionsjson', models.JSONField(default=restaurants.models.Product.default_json)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.category')),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant'),
        ),
    ]
