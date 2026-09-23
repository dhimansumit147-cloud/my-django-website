from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "sungreen_solar",
            "0021_alter_batterystoragecategory_options_and_more",
        ),
    ]

    operations = [

        # Remove old text category
        migrations.RemoveField(
            model_name="batterystorage",
            name="category",
        ),

        # Rename temporary ForeignKey
        migrations.RenameField(
            model_name="batterystorage",
            old_name="category_new",
            new_name="category",
        ),
    ]
