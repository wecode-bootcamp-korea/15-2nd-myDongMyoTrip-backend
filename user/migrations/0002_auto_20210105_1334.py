# Generated by Django 3.1.4 on 2021-01-05 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='social_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='social_platform',
        ),
        migrations.AddField(
            model_name='socialplatform',
            name='social_id',
            field=models.CharField(default=None, max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='socialplatform',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]