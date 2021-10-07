# Generated by Django 3.2.7 on 2021-10-06 14:42

from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0003_alter_productreview_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('total_sum', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order_status', model_utils.fields.StatusField(choices=[('In Progress', 'In Progress'), ('Canceled', 'Canceled'), ('Finished', 'Finished')], default='In Progress', max_length=100, no_check_for_status=True)),
            ],
            options={
                'db_table': 'order',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='items', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='order_items', to='product.product')),
            ],
            options={
                'db_table': 'order_items',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='order.OrderItem', to='product.Product'),
        ),
    ]