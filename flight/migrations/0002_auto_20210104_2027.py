# Generated by Django 3.1.4 on 2021-01-04 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flight', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightbookinginformation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AddField(
            model_name='flight',
            name='airline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.airline'),
        ),
        migrations.AddField(
            model_name='flight',
            name='arrival_airport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival', to='flight.airport'),
        ),
        migrations.AddField(
            model_name='flight',
            name='departure_airport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure', to='flight.airport'),
        ),
        migrations.AddField(
            model_name='flight',
            name='detailed_price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.detailedprice'),
        ),
        migrations.AddField(
            model_name='flight',
            name='seat_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.seatclass'),
        ),
        migrations.AddField(
            model_name='airport',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.region'),
        ),
    ]
