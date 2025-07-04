# Generated by Django 5.2.1 on 2025-06-03 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0002_datatab4"),
    ]

    operations = [
        migrations.CreateModel(
            name="DataTab5OT",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("empId", models.CharField(max_length=200)),
                ("date_start", models.DateTimeField()),
                ("date_end", models.DateTimeField()),
                ("purpose", models.CharField(max_length=1000)),
                ("employment_status", models.CharField(max_length=200)),
                ("office_alias", models.CharField(max_length=200)),
                ("office_name", models.CharField(max_length=200)),
                ("job_level", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="DataTab5Travel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("empId", models.CharField(max_length=200)),
                ("date_from", models.DateField()),
                ("date_to", models.DateField()),
                ("purpose", models.CharField(max_length=1000)),
                ("destintion", models.CharField(max_length=200)),
                ("employment_status", models.CharField(max_length=200)),
                ("office_alias", models.CharField(max_length=200)),
                ("office_name", models.CharField(max_length=200)),
                ("job_level", models.CharField(max_length=200)),
                ("travel_durations", models.IntegerField()),
            ],
        ),
    ]
