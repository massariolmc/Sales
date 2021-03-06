# Generated by Django 3.0.7 on 2020-07-17 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
                ('fantasy_name', models.CharField(blank=True, max_length=100, verbose_name='Nome Fantasia')),
                ('cnpj', models.CharField(max_length=14, unique=True, verbose_name='CNPJ')),
                ('number_state', models.CharField(blank=True, max_length=30, verbose_name='Inscrição Estadual')),
                ('email', models.EmailField(blank=True, max_length=100, unique=True, verbose_name='Email')),
                ('slug', models.SlugField(blank=True, verbose_name='Atalho')),
                ('image', models.ImageField(blank=True, upload_to='media/company/', verbose_name='Imagem')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='Endereço')),
                ('address_number', models.CharField(blank=True, max_length=100, verbose_name='Número')),
                ('neighborhood', models.CharField(blank=True, max_length=100, verbose_name='Bairro')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='Cidade')),
                ('state', models.CharField(blank=True, max_length=100, verbose_name='Estado')),
                ('zip_code', models.CharField(blank=True, max_length=8, verbose_name='CEP')),
                ('phone_1', models.CharField(blank=True, max_length=20, verbose_name='Telefone Principal')),
                ('phone_2', models.CharField(blank=True, max_length=20, verbose_name='Telefone Secundário')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('user_updated', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MaxDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('discount', models.CharField(max_length=100, verbose_name='Desconto')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('slug', models.SlugField(blank=True, verbose_name='Atalho')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='max_discount_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('user_updated', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='max_discount_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
            ],
            options={
                'verbose_name': 'MaxDiscount',
                'verbose_name_plural': 'MaxDiscounts',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PersonType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('slug', models.SlugField(blank=True, verbose_name='Atalho')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('max_discount', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='person.MaxDiscount', verbose_name='Desconto Max')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_type_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('user_updated', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_type_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
            ],
            options={
                'verbose_name': 'PersonType',
                'verbose_name_plural': 'PersonTypes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('abbreviation', models.CharField(blank=True, max_length=100, verbose_name='Sigla')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('slug', models.SlugField(blank=True, verbose_name='Atalho')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='person.Company', verbose_name='Empresa')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='department_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Criado por')),
                ('user_updated', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='department_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Atualizado por')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
                'ordering': ['name'],
            },
        ),
    ]
