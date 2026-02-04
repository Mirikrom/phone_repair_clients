# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0005_laminat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairorder',
            name='client_phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Klent telefon raqami'),
        ),
    ]
