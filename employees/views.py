from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from employees.models import Employee
from employees.serializer import EmployeeSerializer


class EmployeesViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Employee model
    """
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class BusyEmployeesListAPIView(ListAPIView):
    """Special APIView for displaying a list of busiest employees sorted by their tasks"""
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.annotate(tasks_count=Count('task', filter=Q(task__is_active=True))).order_by(
            '-tasks_count')
