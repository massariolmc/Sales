# Generated by Django 3.0.7 on 2020-07-24 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('person', '0002_auto_20200723_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='image',
            field=models.ImageField(blank=True, max_length=200, upload_to='company/', verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='company',
            name='user_created',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='company_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Criado por'),
        ),
        migrations.AlterField(
            model_name='company',
            name='user_updated',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='company_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por'),
        ),
        migrations.AlterField(
            model_name='department',
            name='user_created',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='department_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Criado por'),
        ),
        migrations.AlterField(
            model_name='department',
            name='user_updated',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='department_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por'),
        ),
        migrations.AlterField(
            model_name='maxdiscount',
            name='user_created',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='max_discount_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Criado por'),
        ),
        migrations.AlterField(
            model_name='maxdiscount',
            name='user_updated',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='max_discount_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por'),
        ),
        migrations.AlterField(
            model_name='persontype',
            name='user_created',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='person_type_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Criado por'),
        ),
        migrations.AlterField(
            model_name='persontype',
            name='user_updated',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='person_type_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por'),
        ),
    ]
