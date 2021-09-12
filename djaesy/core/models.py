from crum import get_current_user
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class CreatedByModel(models.Model):

    created_on = models.DateTimeField(_('Criado em'), auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Criado por'),
        editable=False,
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    modified_on = models.DateTimeField(_('Última alteração'), auto_now=True, editable=False)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Alterado por'),
        editable=False,
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        abstract = True

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    def save(self, *args, **kwargs):

        user = get_current_user()

        if user and not user.pk:
            user = None

        if self._state.adding:
            self.created_on = timezone.now()
            self.created_by = user
        else:
            loaded_values = getattr(self, '_loaded_values', None)
            if loaded_values:
                if self.created_by_id != loaded_values['created_by_id']:
                    raise ValueError(_("Atualizar o valor do campo Criado Por não é permitido."))

        self.modified_on = timezone.now()
        self.modified_by = user

        super().save()


