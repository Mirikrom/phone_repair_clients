# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0006_client_phone_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairorder',
            name='status',
            field=models.CharField(
                choices=[
                    ('in_progress', "Ta'mirlanmoqda"),
                    ('ready', 'Tayyor'),
                    ('completed', 'Olib ketilgan'),
                ],
                default='in_progress',
                max_length=20,
                verbose_name='Status'
            ),
        ),
    ]
