# Generated manually — faqat yangi jadval qo'shadi, mavjud ma'lumotlarni o'chirmaydi.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repairs', '0021_repairorder_remind_at_repairorder_reminder_fired_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabelPrintJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[('oddiy', 'Oddiy'), ('tuzalgan', 'Tuzalgan'), ('tuzalmagan', 'Tuzalmagan')], default='oddiy', max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Kutilmoqda'), ('printing', 'Chop etilmoqda'), ('done', 'Chop etildi'), ('failed', 'Xato')], db_index=True, default='pending', max_length=20)),
                ('phone_model', models.CharField(blank=True, max_length=200)),
                ('required_parts', models.CharField(blank=True, max_length=300)),
                ('client_phone', models.CharField(blank=True, max_length=20)),
                ('client_name', models.CharField(blank=True, max_length=200)),
                ('repair_cost', models.CharField(blank=True, max_length=40)),
                ('deposit_amount', models.CharField(blank=True, max_length=40)),
                ('order_created_at', models.DateTimeField(blank=True, null=True)),
                ('printed_at_client', models.DateTimeField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('repair_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='label_print_jobs', to='repairs.repairorder')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='label_print_jobs', to='repairs.shop')),
            ],
            options={
                'verbose_name': 'Etiketka pechat navbati',
                'verbose_name_plural': 'Etiketka pechat navbati',
                'ordering': ['created_at'],
            },
        ),
    ]
