# Generated by Django 3.2.12 on 2022-12-17 01:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to='accounts.user')),
                ('comment', models.CharField(blank=True, max_length=255, verbose_name='コメント')),
            ],
            options={
                'db_table': 'Profile',
            },
        ),
        migrations.CreateModel(
            name='FriendShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='friendship',
            constraint=models.UniqueConstraint(fields=('following', 'follower'), name='follow_unique'),
        ),
    ]
