# Generated by Django 4.2.11 on 2024-04-18 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LLMTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_input', models.CharField(max_length=200)),
                ('answer', models.TextField()),
            ],
        ),
    ]