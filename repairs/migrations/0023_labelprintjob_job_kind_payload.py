from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0022_label_print_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='labelprintjob',
            name='job_kind',
            field=models.CharField(
                choices=[
                    ('label', 'Etiketka'),
                    ('vizitka', 'Vizitka'),
                    ('carta', 'Karta nomer'),
                    ('zapchast', "Zapchast ro'yxati"),
                ],
                db_index=True,
                default='label',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='labelprintjob',
            name='printer_target',
            field=models.CharField(
                choices=[
                    ('label', 'Etiketka printer (T361U)'),
                    ('receipt', 'Chek printer (XP-80)'),
                ],
                default='label',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='labelprintjob',
            name='payload',
            field=models.TextField(blank=True, help_text='JSON (zapchast items va boshqalar)'),
        ),
        migrations.AlterModelOptions(
            name='labelprintjob',
            options={
                'ordering': ['created_at'],
                'verbose_name': 'Pechat navbati',
                'verbose_name_plural': 'Pechat navbati',
            },
        ),
    ]
