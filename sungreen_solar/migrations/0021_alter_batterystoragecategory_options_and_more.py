from django.db import migrations


def convert_old_categories(apps, schema_editor):

    BatteryStorage = apps.get_model(
        "sungreen_solar",
        "BatteryStorage"
    )

    BatteryStorageCategory = apps.get_model(
        "sungreen_solar",
        "BatteryStorageCategory"
    )

    batteries = BatteryStorage.objects.all()

    for battery in batteries:

        old_category = battery.category

        if not old_category:
            continue

        old_category = old_category.strip()

        if not old_category:
            continue

        category, created = BatteryStorageCategory.objects.get_or_create(
            name=old_category
        )

        battery.category_new_id = category.id

        battery.save(
            update_fields=["category_new"]
        )


class Migration(migrations.Migration):

    dependencies = [
        (
            "sungreen_solar",
            "0020_batterystoragecategory_alter_batterystorage_category",
        ),
    ]

    operations = [

        migrations.RunPython(
            convert_old_categories,
            migrations.RunPython.noop,
        ),
    ]
