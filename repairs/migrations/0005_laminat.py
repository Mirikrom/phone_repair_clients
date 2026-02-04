# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0004_add_kbs_kaiku'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairorder',
            name='laminat',
            field=models.CharField(
                blank=True,
                choices=[('laminat', "Laminatsiya qo'yib berish"), ('laminatsiz', 'Laminatsiya shart emas')],
                max_length=20,
                verbose_name='Laminat'
            ),
        ),
    ]
