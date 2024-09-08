from django.db import models
from employees.models import NULLABLE, Employee

CREATED = 'created'
ASSIGNED = 'assigned'
COMPLETE = 'complete'
PAUSED = 'paused'
CANCELLED = 'cancelled'
STATUS = (
    (CREATED, 'created'),
    (ASSIGNED, 'assigned'),
    (COMPLETE, 'complete'),
    (PAUSED, 'paused'),
    (CANCELLED, 'cancelled')
)

LOW = 'low'
MIDDLE = 'middle'
HIGH = 'high'
URGENCY = (
    (LOW, 'low'),
    (MIDDLE, 'middle'),
    (HIGH, 'high')
)


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    parent_task = models.ForeignKey('self', default=None, on_delete=models.CASCADE, **NULLABLE,
                                    verbose_name='parent_task')
    employee = models.ForeignKey(Employee, default=None, on_delete=models.SET_NULL, **NULLABLE, verbose_name='executor')
    target_date = models.DateTimeField(**NULLABLE, verbose_name='target date')
    status = models.CharField(choices=STATUS, default=CREATED, verbose_name='task status')
    urgency = models.CharField(choices=URGENCY, default=LOW, verbose_name='urgency')
    importance = models.CharField(choices=URGENCY, default=LOW, verbose_name='importance')
    is_active = models.BooleanField(default=True, verbose_name='task activity')

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ('name', 'employee', 'target_date', 'status', 'urgency', 'importance')
