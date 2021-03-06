# Generated by Django 3.0.7 on 2020-07-29 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('person', '0004_auto_20200728_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Name')),
                ('birthday', models.DateField(blank=True, max_length=100, verbose_name='Birthday')),
                ('gender', models.CharField(blank=True, choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')], max_length=50, verbose_name='Gender')),
                ('fathers_name', models.CharField(blank=True, max_length=100, verbose_name='Fathes Name')),
                ('mothers_name', models.CharField(blank=True, max_length=100, verbose_name='Mothers Name')),
                ('blood_type', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=10, verbose_name='Blood Type')),
                ('rg', models.CharField(blank=True, help_text='Apenas números', max_length=50, verbose_name='General Register Number ')),
                ('rg_exped', models.CharField(blank=True, help_text='Ex: SSP / DETRAN / FORÇAS ARMADAS / CREA / OAB', max_length=100, verbose_name='Instituition')),
                ('rg_uf', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=50, verbose_name='United')),
                ('birthplace', models.CharField(blank=True, max_length=100, verbose_name='Birthplace')),
                ('birthplace_state', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=100, verbose_name='Birthplace - State')),
                ('maritalstatus', models.CharField(blank=True, choices=[('Casado', 'Casado'), ('Solteiro', 'Solteiro'), ('Divorciado', 'Divorciado'), ('Viúvo', 'Viúvo')], max_length=100, verbose_name='Marital Status')),
                ('pis_pasep', models.CharField(blank=True, help_text='Apenas Números', max_length=100, verbose_name='PIS/PASEP')),
                ('work_portifolio_number', models.CharField(blank=True, help_text='Apenas Números', max_length=100, verbose_name='Work Portifolio Number')),
                ('work_portifolio_serie', models.CharField(blank=True, help_text='Apenas Números', max_length=100, verbose_name='Work Portifolio Serie')),
                ('work_portifolio_state', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], help_text='Apenas Números', max_length=100, verbose_name='Work Portifolio State')),
                ('voter_title_number', models.CharField(blank=True, help_text='Apenas Números', max_length=50, verbose_name='Voter Title Number')),
                ('voter_title_zone', models.CharField(blank=True, help_text='Apenas Números', max_length=10, verbose_name='Voter Title Zone')),
                ('voter_title_section', models.CharField(blank=True, help_text='Apenas Números', max_length=10, verbose_name='Voter Title Section')),
                ('voter_title_state', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='Voter Title State')),
                ('drivers_license_number', models.CharField(blank=True, help_text='Apenas Números', max_length=50, verbose_name='Drivers License')),
                ('drivers_license_state', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='Drivers License State')),
                ('drivers_license_validate', models.DateField(blank=True, max_length=20, verbose_name='Drivers License - Validate')),
                ('drivers_license_category', models.CharField(blank=True, choices=[('A', 'A'), ('AB', 'AB'), ('AC', 'AC'), ('AD', 'AD'), ('AE', 'AE'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=2, verbose_name='Drivers License - Category')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='Address')),
                ('address_number', models.CharField(blank=True, help_text='Apenas Números', max_length=10, verbose_name='Address Number')),
                ('address_neighborhood', models.CharField(blank=True, max_length=100, verbose_name='Address Neighborhood')),
                ('address_city', models.CharField(blank=True, max_length=100, verbose_name='City')),
                ('address_state', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=100, verbose_name='State')),
                ('zip_code', models.CharField(blank=True, help_text='Apenas Números', max_length=8, verbose_name='Zip Code')),
                ('phone_1', models.CharField(blank=True, max_length=20, verbose_name='Main Phone')),
                ('phone_2', models.CharField(blank=True, max_length=20, verbose_name='Secundary Phone')),
                ('image', models.ImageField(blank=True, max_length=200, upload_to='person/', verbose_name='Image')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='person.Department', verbose_name='Department')),
                ('person_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='person.PersonType', verbose_name='Person Type')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='person_user_login', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('user_created', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='person_user_created_id', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('user_updated', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='person_user_updated_id', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
                'ordering': ['name'],
            },
        ),
    ]
