# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0002_ready_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairorder',
            name='required_parts',
            field=models.CharField(blank=True, max_length=300, verbose_name="Qo'yilish kerak bo'lgan zapchast"),
        ),
        migrations.AddField(
            model_name='repairorder',
            name='screen_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('incell_abadoksiz', 'Incell abadoksiz'),
                    ('incell_abadokli', 'Incell abadokli'),
                    ('oled_abadokli', 'OLED abadokli'),
                    ('oled_abadoksiz', 'OLED abadoksiz'),
                    ('original_abadokli', 'Original abadokli'),
                    ('original_abadoksiz', 'Original abadoksiz'),
                ],
                max_length=30,
                verbose_name='Ekran turi'
            ),
        ),
    ]
