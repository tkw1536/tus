# Generated by Django 4.2 on 2023-04-14 15:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tus", "0003_alter_shorturl_permanent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shorturl",
            name="slug",
            field=models.CharField(
                blank=True,
                help_text="Slug to forward from",
                max_length=500,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="staticpage",
            name="slug",
            field=models.CharField(
                blank=True,
                help_text="Slug to forward from",
                max_length=500,
                unique=True,
            ),
        ),
    ]
