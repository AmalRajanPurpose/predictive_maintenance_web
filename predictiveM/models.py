from django.db import models


# Create your models here.


class Allocate(models.Model):
    id = models.AutoField(primary_key=True)
    date_of_maintenance = models.DateField()
    machine_name = models.CharField(null=True, max_length=50)
    is_allocate_or_not = models.CharField(max_length=50, blank=True, null=True)

    def __int__(self):
        return self.id
