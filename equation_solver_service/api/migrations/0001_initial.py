# Generated by Django 4.1.2 on 2024-06-09 23:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('equation', models.CharField(max_length=255)),
                ('solution', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
