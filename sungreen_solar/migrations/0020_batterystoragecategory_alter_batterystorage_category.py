from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        (
            "sungreen_solar",
            "0019_batterystorage_category_batterystorage_inverter",
        ),
    ]

    operations = [

        migrations.CreateModel(
            name="BatteryStorageCategory",
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
                (
                    "name",
                    models.CharField(
                        max_length=200,
                        unique=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now
                    ),
                ),
            ],
        ),

        # Temporary ForeignKey
        migrations.AddField(
            model_name="batterystorage",
            name="category_new",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.SET_NULL,
                related_name="battery_storages_new",
                to="sungreen_solar.batterystoragecategory",
            ),
        ),
    ]
