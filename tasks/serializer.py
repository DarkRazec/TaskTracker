from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task objects"""
    target_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def validate_parent_task(self, value):
        """Validator for parent_task field"""

        if self.instance:
            if self.instance.id == value.id:
                raise serializers.ValidationError("A task cannot be referred to itself.")
            elif self.instance.parent_task and (value is None or value.id != self.instance.parent_task.id):
                raise serializers.ValidationError("A child task cannot be unassigned from a parent task.")

        elif value.status in ('created', 'cancelled'):
            raise serializers.ValidationError("A task cannot be created for a cancelled or unassigned parent task.")

        return value


class ImportantTaskSerializer(serializers.Serializer):
    """Serializer for Task objects that have parent tasks but no assigned employee"""
    target_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')

    def to_representation(self, instance):
        # Checks whether the parent task employee has been assigned a maximum of 2 more tasks than the employee
        if instance.parent_task.employee.task_set.count() - self.context['employee'].tasks_count <= 2:
            employee = instance.parent_task.employee  # parent task employee
        else:
            employee = self.context['employee']  # least loaded employee

        return {
            'task_id': instance.id,
            'target_date': self.fields['target_date'].to_representation(instance.target_date),
            'full_name': [employee.last_name, employee.first_name, employee.middle_name]
        }
