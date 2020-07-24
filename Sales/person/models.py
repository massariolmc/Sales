from django.db import models
from django.utils.translation import ugettext_lazy as _
from Sales.account.models import User
from .compress_image import compress, delete_old_image
from .slug_file import unique_uuid


class Company(models.Model):
    name = models.CharField(_('Nome'), max_length=100, unique=True, blank=False, null=False)
    fantasy_name = models.CharField(_('Nome Fantasia'), max_length=100, blank=True)
    cnpj = models.CharField(_('CNPJ'), max_length=14, unique=True, blank=False, null=False)
    number_state = models.CharField(_('Inscrição Estadual'), max_length=30, blank=True)
    email = models.EmailField(_('Email'), max_length=100, unique=True, blank=True)    
    slug = models.SlugField(_('Atalho'), max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to = 'company/', verbose_name =
            'Imagem', blank=True, max_length=200)
    description = models.TextField(_('Descrição'), blank=True)        
    address = models.CharField(_("Endereço"), max_length=100, blank=True)
    address_number = models.CharField(_("Número"), max_length=100, blank=True)
    neighborhood = models.CharField(_("Bairro"), max_length=100, blank=True)
    city = models.CharField(_("Cidade"), max_length=100, blank=True)
    state = models.CharField(_("Estado"), max_length=2, blank=True)
    zip_code = models.CharField(_("CEP"), max_length=8, blank=True)
    phone_1 = models.CharField(_("Telefone Principal"), max_length=20, blank=True)
    phone_2 = models.CharField(_("Telefone Secundário"), max_length=20, blank=True)
    user_created = models.ForeignKey(User, related_name="company_user_created_id", verbose_name=_("Criado por"), on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="company_user_updated_id", verbose_name=_("Atualizado por"), on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Criado em'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]   

    def save(self, *args, **kwargs):        
        if self.id:
            #Deleta a imagem antiga, caso não for igual
            delete_old_image(self.__class__, self.id, self.image)            
        else:
            #Insere um valor para o Slug            
            self.slug = unique_uuid()        
        
        # Comprime a imagem
        if self.image:
            new_image = compress(self.image)                
            self.image = new_image           
        # save
        super().save(*args, **kwargs)

    # Sobreescreve este metodo para delete imagens. Sem a imagem continua em media, mesmo deletando a pessoa do banco
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(_("Nome"), max_length=100, blank=False, null= False)
    abbreviation = models.CharField(_("Sigla"), max_length=100, blank=True)
    description = models.TextField(_('Descrição'), blank=True)  
    slug = models.SlugField(_('Atalho'), blank=True)      
    company = models.ForeignKey(Company, verbose_name=_("Empresa"), on_delete=models.PROTECT, blank=False, null= False)
    user_created = models.ForeignKey(User, related_name="department_user_created_id", verbose_name=_("Criado por"), on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="department_user_updated_id", verbose_name=_("Atualizado por"), on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Criado em'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ["name"]
    
    def __str__(self):
        return self.name

class MaxDiscount(models.Model):
    name = models.CharField(_("Nome"), max_length=100, blank=False, null= False)
    discount = models.CharField(_("Desconto"), max_length=100, blank=False, null= False)    
    description = models.TextField(_('Descrição'), blank=True)  
    slug = models.SlugField(_('Atalho'), blank=True)          
    user_created = models.ForeignKey(User, related_name="max_discount_user_created_id", verbose_name=_("Criado por"), on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="max_discount_user_updated_id", verbose_name=_("Atualizado por"), on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Criado em'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)
    class Meta:
        verbose_name = "MaxDiscount"
        verbose_name_plural = "MaxDiscounts"
        ordering = ["name"]
    
    def __str__(self):
        return self.name

class PersonType(models.Model):
    name = models.CharField(_("Nome"), max_length=100, blank=False, null= False)        
    description = models.TextField(_('Descrição'), blank=True)  
    max_discount = models.ForeignKey(MaxDiscount, verbose_name=_("Desconto Max"), on_delete=models.PROTECT)
    slug = models.SlugField(_('Atalho'), blank=True)          
    user_created = models.ForeignKey(User, related_name="person_type_user_created_id", verbose_name=_("Criado por"), on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="person_type_user_updated_id", verbose_name=_("Atualizado por"), on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Criado em'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Atualizado em'), auto_now=True)
    class Meta:
        verbose_name = "PersonType"
        verbose_name_plural = "PersonTypes"
        ordering = ["name"]
    
    def __str__(self):
        return self.name
