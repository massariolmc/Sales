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

class Person(models.Model):
    gender_choices = [("Masculino","Masculino"), ("Feminino","Feminino")]
    blood_choices = [("A+","A+"), ("A-","A-"), ("B+","B+"), ("B-","B-"), ("AB+","AB+"), ("AB-","AB-"), ("O+","O+"), ("O-","O-")]
    drivers_license_category_choices = [("A","A"),("AB","AB"),("AC","AC"),("AD","AD"),("AE","AE"),("B","B"),("C","C"),("D","D"),("E","E")]
    states_choices = ( ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'), )
    marital_choices = [('Casado','Casado'),('Solteiro','Solteiro'), ('Divorciado','Divorciado'), ('Viúvo','Viúvo')]

    name = models.CharField(_("Name"), max_length=100, blank=True)
    birthday = models.DateField(_("Birthday"), max_length=100, blank=True, null=True)    
    gender = models.CharField(_("Gender"), max_length = 50, choices=gender_choices, blank=True)
    fathers_name = models.CharField(_("Fathes Name"), max_length=100, blank=True)
    mothers_name = models.CharField(_("Mothers Name"), max_length=100, blank=True)    
    blood_type = models.CharField(_("Blood Type"), choices=blood_choices, max_length=10, blank=True)    
    rg = models.CharField(_("General Register Number "), max_length = 50, blank=True, help_text="Apenas números")
    rg_exped = models.CharField(_("Instituition"), max_length = 100,blank=True, help_text="Ex: SSP / DETRAN / FORÇAS ARMADAS / CREA / OAB" )
    rg_uf = models.CharField(_("United"), choices=states_choices, max_length = 50,blank=True )
    birthplace = models.CharField(_("Birthplace"),max_length=100, blank=True)
    birthplace_state = models.CharField(_("Birthplace - State"),max_length=100, choices=states_choices, blank=True)
    maritalstatus = models.CharField(_("Marital Status"), choices=marital_choices, max_length=100, blank=True)        
    pis_pasep = models.CharField(_("PIS/PASEP"), max_length=100, blank=True, help_text = "Apenas Números")
    work_portifolio_number = models.CharField(_("Work Portifolio Number"), max_length=100, blank=True, help_text = "Apenas Números")
    work_portifolio_serie = models.CharField(_("Work Portifolio Serie"), max_length=100, blank=True, help_text = "Apenas Números")
    work_portifolio_state = models.CharField(_("Work Portifolio State"), max_length=100, choices=states_choices, blank=True, help_text = "Apenas Números")
    voter_title_number = models.CharField(_("Voter Title Number"), max_length=50, blank=True, help_text = "Apenas Números")
    voter_title_zone = models.CharField(_("Voter Title Zone"), max_length=10, blank=True, help_text = "Apenas Números")
    voter_title_section = models.CharField(_("Voter Title Section"), max_length=10, blank=True, help_text = "Apenas Números")
    voter_title_state = models.CharField(_("Voter Title State"), choices=states_choices, max_length = 2, blank=True )    
    drivers_license_number = models.CharField(_("Drivers License"), max_length=50, blank=True, help_text = "Apenas Números")
    drivers_license_state = models.CharField(_("Drivers License State"), choices=states_choices, max_length = 2, blank=True)
    drivers_license_validate = models.DateField(_("Drivers License - Validate"), max_length=20, blank=True, null=True)
    drivers_license_category = models.CharField(_("Drivers License - Category"), choices=drivers_license_category_choices, max_length=2, blank=True)
    address = models.CharField(_("Address"), max_length=100, blank=True)
    address_number = models.CharField(_("Address Number"), max_length=10, blank=True, help_text="Apenas Números")
    address_neighborhood = models.CharField(_("Address Neighborhood"), max_length=100, blank=True)
    address_city = models.CharField(_("City"), max_length=100, blank=True)
    address_state = models.CharField(_("State"), max_length=100, choices=states_choices, blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=8, blank=True, help_text = "Apenas Números")        
    phone_1 = models.CharField(_("Main Phone"), max_length=20, blank=True)
    phone_2 = models.CharField(_("Secundary Phone"), max_length=20, blank=True)    
    image = models.ImageField(upload_to = 'person/', verbose_name =
            _('Image'), blank=True, max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)    
    user = models.OneToOneField(User, related_name="person_user_login", verbose_name=_("User"), blank=False, null= False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True) 
    user_created = models.ForeignKey(User, related_name="person_user_created_id", verbose_name=_("Created by"), blank=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="person_user_updated_id", verbose_name=_("Updated by"), blank=True, on_delete=models.PROTECT)    
    
    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")
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

class Position(models.Model):
    name = models.CharField(_("Name"), max_length=100, blank=False, null= False)        
    description = models.TextField(_('Description'), blank=True)      
    slug = models.SlugField(_('Slug'), blank=True)     
    department = models.ForeignKey(Department, verbose_name=_("Department"), on_delete=models.PROTECT, blank=False, null= False)         
    members = models.ManyToManyField(Person, through='PersonPosition')
    user_created = models.ForeignKey(User, related_name="person_type_user_created_id", verbose_name=_("Created by"), blank=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="person_type_user_updated_id", verbose_name=_("Updated by"), blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    class Meta:
        verbose_name = _("Situation")
        verbose_name_plural = _("Situations")
        ordering = ["name"]
    
    def save(self, *args, **kwargs):        
                    
        if not self.id:
            #Insere um valor para o Slug            
            self.slug = unique_uuid(self.__class__)               
        # save
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class PersonPosition(models.Model):
    active = models.BooleanField(_("Active"), default=True, blank=False, null= False)        
    person = models.ForeignKey(Person, verbose_name=_("person"), on_delete=models.PROTECT, blank=False, null= False)         
    position = models.ForeignKey(Position, verbose_name=_("position"), on_delete=models.PROTECT, blank=False, null= False)         
    slug = models.SlugField(_('Slug'), blank=True)         
    user_created = models.ForeignKey(User, related_name="person_position_user_created_id", verbose_name=_("Created by"), blank=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="person_position_user_updated_id", verbose_name=_("Updated by"), blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    class Meta:
        verbose_name = _("PersonPosition")
        verbose_name_plural = _("PersonPositions")
        ordering = ["person"]
    
    def save(self, *args, **kwargs):        
                    
        if not self.id:
            #Insere um valor para o Slug            
            self.slug = unique_uuid(self.__class__)               
        # save
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.person.name