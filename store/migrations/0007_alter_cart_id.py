# Cart IDs are UUIDs from the initial migration. This migration remains in the
# chain for databases that have already recorded the earlier migration history.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20210903_1318'),
    ]

    operations = []
