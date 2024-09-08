from datetime import datetime, timedelta

from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from employees.models import Employee
from tasks.models import Task, ASSIGNED, CREATED
from tasks.serializer import TaskSerializer, ImportantTaskSerializer


class TaskViewSet(ModelViewSet):
    """ViewSet for Employee model"""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        self.object = serializer.save()
        if self.object.target_date is None:
            self.object.target_date = datetime.today() + timedelta(days=2)
        if self.object.employee:
            self.object.status = ASSIGNED
        else:
            self.object.status = CREATED
        self.object.save()

    def perform_update(self, serializer):
        self.object = serializer.save()
        match self.object.status:
            case 'created' | 'assigned':
                self.object.status = ASSIGNED if self.object.employee else CREATED
            case 'cancelled' | 'complete':
                self.object.is_active = False
        self.object.save()


class ImportantTasksListAPIView(ListAPIView):
    """Special APIView for displaying important tasks"""

    serializer_class = ImportantTaskSerializer
    queryset = Task.objects.filter(parent_task__isnull=False, employee__isnull=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['employee'] = Employee.objects.annotate(tasks_count=Count('task')).order_by('tasks_count').first()
        return context

