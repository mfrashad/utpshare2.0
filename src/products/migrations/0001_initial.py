# Generated by Django 2.0.7 on 2018-07-18 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('stock_count', models.PositiveSmallIntegerField(default=1)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.SellerAccount')),
            ],
        ),
    ]
