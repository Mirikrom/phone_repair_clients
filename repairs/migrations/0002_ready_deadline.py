# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repairorder',
            name='ready_date',
        ),
        migrations.AddField(
            model_name='repairorder',
            name='ready_deadline',
            field=models.CharField(
                blank=True,
                choices=[
                    ('today_evening', 'Bugun kechga'),
                    ('tomorrow_evening', 'Ertaga kechga'),
                    ('2_3_days', '2-3 kundan keyin'),
                ],
                max_length=20,
                verbose_name="Tayyor bo'lish muddati"
            ),
        ),
    ]
