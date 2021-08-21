from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractUser, Group, Permission
from django.db import models

UserRoleClass = getattr(settings, 'DJAESY_USER_ROLE_CLASS', 'djaesy.Role')


class PermissionManager(models.Manager):
    def get_queryset(self):
        return super(PermissionManager, self).get_queryset()


class CustomPermission(Permission):

    objects = PermissionManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Role(Group):

    class Meta:
        verbose_name = _('Perfil de Acesso')
        verbose_name_plural = _('Perfís de Acesso')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True, db_index=True, verbose_name=_('Email'))
    name = models.CharField(max_length=255, verbose_name=_('Nome'))

    role = models.ForeignKey(
        UserRoleClass, null=True, blank=True, related_name='user_roles', on_delete=models.PROTECT,
        db_index=True, verbose_name=_('Perfil de Permissão')
    )

    user_type = models.CharField(
        max_length=12, verbose_name=_('Tipo de Usuário'), choices=settings.DJAESY_USER_TYPES,
        default=settings.DJAESY_DEFAULT_USER_TYPE
    )

    must_change_password = models.BooleanField(
        default=False, verbose_name="Mudar senha",
        help_text="Usuário será forçado a definir uma nova senha no próximo acesso."
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role:
            self.groups.clear()
            self.groups.add(self.role)
        else:
            self.groups.clear()
