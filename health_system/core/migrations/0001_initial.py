# Generated by Django 5.1.7 on 2025-03-16 16:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DailyFoodLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.CharField(max_length=20)),
                ('food_description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='UserQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_text', models.TextField()),
                ('response', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='WellnessCoach',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('specialization', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wellness_coach',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.wellnesscoach'),
        ),
        migrations.CreateModel(
            name='CoachReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.userprofile')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.wellnesscoach')),
            ],
        ),
    ]
