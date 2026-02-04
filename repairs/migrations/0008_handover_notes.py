# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0007_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairorder',
            name='handover_notes',
            field=models.TextField(blank=True, verbose_name="Olib ketilganda eslatma (qarz bo'lsa)"),
        ),
    ]
