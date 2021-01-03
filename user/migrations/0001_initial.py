# Generated by Django 3.1.4 on 2021-01-02 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialPlatform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'social_platforms',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=250)),
                ('is_location_agreed', models.BooleanField(default=False)),
                ('is_promotion_agreed', models.BooleanField(default=False)),
                ('social_id', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('social_platform', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.socialplatform')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='RecentView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.flight')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'recent_views',
            },
        ),
    ]
