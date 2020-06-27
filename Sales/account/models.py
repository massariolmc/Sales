from django.db import models
import re
from django.db import models
from django.db.models.signals import post_save
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.conf import settings
import datetime
# Create your models here.

class UserManager(BaseUserManager):    
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
           
        
    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)    
    
    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, True, True, **extra_fields)               
        return user

class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(_('username'), max_length=15, unique=True, help_text=_('Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters'), validators=[ validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid'))])
    cpf = models.CharField(_('CPF'), max_length=11, unique=True, help_text=_('Required. 11 digits exactly'))  
    first_name = models.CharField(_('first name'), max_length=30)    
    last_name = models.CharField(_('last name'), max_length=30)    
    email = models.EmailField(_('email address'), max_length=255, unique=True)    
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_trusty = models.BooleanField(_('trusty'), default=False, help_text=_('Designates whether this user has confirmed his account.'))
    date_login = models.DateTimeField(_('date login'), blank=True, null=True)
    date_logout = models.DateTimeField(_('date logout'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now_add=False, auto_now=True)
    user_created = models.ForeignKey('self', related_name="user_user_created_id", verbose_name=_("Created by "), null=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey('self', related_name="user_user_updated_id", verbose_name=_("Updated by "), null=True, on_delete=models.PROTECT)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','email']

    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return 'cpf:{} - Username: {} - First Name: {} - Last Name - {} - email: {}'.format(self.cpf,self.username,self.first_name, self.last_name, self.email)
        
    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        return self.first_name
    
    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])


def login_user(sender, request, user, **kwargs):
    acesso = User.objects.get(pk=user.id)
    acesso.date_login = datetime.datetime.now()  
    acesso.save()

def logout_user(sender, request, user, **kwargs):
    acesso = User.objects.get(pk=user.id)
    acesso.date_logout = datetime.datetime.now()    
    acesso.save()

 

#Signals
user_logged_in.connect(login_user)
user_logged_out.connect(logout_user)
