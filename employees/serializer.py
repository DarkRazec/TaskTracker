from rest_framework.serializers import ModelSerializer

from employees.models import Employee
from tasks.serializer import TaskSerializer


class EmployeeSerializer(ModelSerializer):
    """Serializer for Employee objects"""
    tasks = TaskSerializer(source='task_set', many=True, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
