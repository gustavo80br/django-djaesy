from django.db import models

# Create your models here.


class TabA(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return f'--*-- {self.name} --*--'


class TabB(models.Model):

    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    relationship = models.ForeignKey(TabA, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('-name',)
        unique_together = ['name', 'description']
