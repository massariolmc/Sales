from django.db import models
from django.utils.translation import ugettext_lazy as _
from Sales.account.models import User
from .compress_image import compress, delete_old_image
from .slug_file import unique_uuid


class Company(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True, blank=False, null=False)
    fantasy_name = models.CharField(_('Fantasy Name'), max_length=100, blank=True)
    cnpj = models.CharField(_('CNPJ'), max_length=14, unique=True, blank=False, null=False)
    number_state = models.CharField(_('Number State'), max_length=30, blank=True)
    email = models.EmailField(_('Email'), max_length=100, unique=True, blank=True)    
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to = 'company/', verbose_name =
            _('Image'), blank=True, max_length=200)
    description = models.TextField(_('Description'), blank=True)        
    address = models.CharField(_("Address"), max_length=100, blank=True)
    address_number = models.CharField(_("Address Number"), max_length=100, blank=True)
    neighborhood = models.CharField(_("Neighborhood"), max_length=100, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    state = models.CharField(_("State"), max_length=2, blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=8, blank=True)
    phone_1 = models.CharField(_("Main Phone"), max_length=20, blank=True)
    phone_2 = models.CharField(_("Secundary Phone"), max_length=20, blank=True)
    user_created = models.ForeignKey(User, related_name="company_user_created_id", verbose_name=_("Created by"), blank=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="company_user_updated_id", verbose_name=_("Updated by"), blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["name"]   

    def save(self, *args, **kwargs):        
        marc = 0
        if self.id:            
            #Deleta a imagem antiga, caso não for igual
            marc = delete_old_image(self.__class__, self.id, self.image)            
        else:
            #Insere um valor para o Slug            
            self.slug = unique_uuid(self.__class__)        
        
        # Comprime a imagem
        if marc:           
            new_image = compress(self.image)                
            self.image = new_image           
        # save
        super().save(*args, **kwargs)

    # Sobreescreve este metodo para delete imagens. Sem a imagem continua em media, mesmo deletando a pessoa do banco
    def delete(self, *args, **kwargs):
        self.image.delete(save=False)# Se deixar save=True ele deleta o arquivo e chama o metodo save automaticamente e ai isso gerar erro.
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(_("Name"), max_length=100, blank=False, null= False)
    abbreviation = models.CharField(_("Abbreviation"), max_length=100, blank=True)
    description = models.TextField(_('Description'), blank=True)  
    slug = models.SlugField(_('Slug'), blank=True)      
    company = models.ForeignKey(Company, verbose_name=_("Company"), on_delete=models.PROTECT, blank=False, null= False)
    user_created = models.ForeignKey(User, related_name="department_user_created_id", verbose_name=_("Created by"), blank=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="department_user_updated_id", verbose_name=_("Updated By"), blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        ordering = ["name"]
    
    def save(self, *args, **kwargs):        
                    
        if not self.id:
            #Insere um valor para o Slug            
            self.slug = unique_uuid(self.__class__)               
        # save
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class PersonType(models.Model):
    name = models.CharField(_("Name"), max_length=100, blank=False, null= False)        
    description = models.TextField(_('Description'), blank=True)  
    max_discount = models.PositiveIntegerField(_('Discount Max'), blank=False, null=False)
    slug = models.SlugField(_('Slug'), blank=True) 
    block_discount = models.BooleanField(_('Block Discount'), default=True, blank=False, null=False)
    company = models.ForeignKey(Company, verbose_name=_("Company"), default=1, on_delete=models.PROTECT, blank=False, null= False)         
    user_created = models.ForeignKey(User, related_name="person_type_user_created_id", verbose_name=_("Created by"), blank=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="person_type_user_updated_id", verbose_name=_("Updated by"), blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    class Meta:
        verbose_name = _("PersonType")
        verbose_name_plural = _("PersonTypes")
        ordering = ["name"]
    
    def save(self, *args, **kwargs):        
                    
        if not self.id:
            #Insere um valor para o Slug            
            self.slug = unique_uuid(self.__class__)               
        # save
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
