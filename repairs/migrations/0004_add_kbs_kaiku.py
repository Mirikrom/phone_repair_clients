# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0003_required_parts_screen_type'),
    ]

    operations = [
        migrations.AlterField(
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
                    ('kbs', 'KBS'),
                    ('kaiku', 'KAIKU'),
                ],
                max_length=30,
                verbose_name='Ekran turi'
            ),
        ),
    ]
