# Generated migration

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0008_handover_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairorder',
            name='zapchast_olib_kelish_kerak',
            field=models.BooleanField(default=False, verbose_name='Zapchast olib kelish kerak'),
        ),
        migrations.CreateModel(
            name='ZapchastItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Zapchast nomi')),
                ('is_done', models.BooleanField(default=False, verbose_name='Olib kelingan')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('repair_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='zapchast_items', to='repairs.repairorder', verbose_name='Buyurtma')),
            ],
            options={
                'verbose_name': 'Zapchast',
                'verbose_name_plural': 'Zapchastlar',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
