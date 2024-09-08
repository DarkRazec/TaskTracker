from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Employee(models.Model):
    last_name = models.CharField(max_length=50, verbose_name='last name')
    first_name = models.CharField(max_length=50, verbose_name='first name')
    middle_name = models.CharField(max_length=50, verbose_name='middle name/patronymic', **NULLABLE)
    position = models.CharField(max_length=100, verbose_name='position in the company')
    company = models.CharField(max_length=100, verbose_name='company name')
    email = models.EmailField(unique=True, verbose_name='email address')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)

    def __str__(self):
        return f'{self.last_name, self.first_name, self.middle_name, self.email}' if self.middle_name else \
            f'{self.last_name, self.first_name, self.email}'

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ('last_name', 'first_name', 'middle_name', 'email', 'phone')
