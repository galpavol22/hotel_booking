# Generated by Django 4.2.20 on 2025-03-15 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_remove_reservation_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='hotelinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='hotelinfo',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to='booking.room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.TextField(default='Štandardná izba.'),
        ),
        migrations.AlterField(
            model_name='room',
            name='price_per_night',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('single', 'Jednolôžková'), ('double', 'Dvojlôžková'), ('suite', 'Apartmán')], max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
