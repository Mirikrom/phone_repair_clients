from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0023_labelprintjob_job_kind_payload'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairorder',
            name='label_print_mark',
            field=models.CharField(
                blank=True,
                choices=[('', 'Oddiy'), ('tuzalgan', 'Tuzalgan'), ('tuzalmagan', 'Tuzalmagan')],
                default='',
                max_length=20,
                verbose_name='Etiketka pechat belgisi (rang)',
            ),
        ),
    ]
